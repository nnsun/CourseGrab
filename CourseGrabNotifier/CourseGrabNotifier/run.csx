#r "System.Configuration"
#r "System.Data"

using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Http;
using System.Net.Mail;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using HtmlAgilityPack;
using SendGrid;
using SendGrid.Helpers.Mail;


public static void Run(TimerInfo myTimer, TraceWriter log)
{
    // Get the necessary connection variables from environment variables
    string server = Environment.GetEnvironmentVariable("DB_SERVER");
    string database = Environment.GetEnvironmentVariable("DB_NAME");
    string username = Environment.GetEnvironmentVariable("DB_USERNAME");
    string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
    string apiKey = Environment.GetEnvironmentVariable("SENDGRID_API_KEY");

    string connectionString = $@"Server={server},1433;
                                Initial Catalog={database};Persist Security Info=False;
                                User ID={username};Password={password};MultipleActiveResultSets=False;
                                Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

    // Key: course subject code (ie. "AEM"), value: list of IDs of courses in the subject
    Dictionary<string, List<int>> subjectCourseDict = new Dictionary<string, List<int>>();

    // Connect to the database
    using (SqlConnection connection = new SqlConnection(connectionString))
    {
        connection.Open();

        // The next three SQL queries are used to populate subjectCourseDict with
        // all currently tracked courses

        // Select the course number and subject code of all subscribed courses
        string sql = @"SELECT C.CourseNum, C.SubjectCode FROM Subscriptions S
                        INNER JOIN Courses C ON S.CourseNum = C.CourseNum";
        using (SqlCommand command = new SqlCommand(sql, connection))
        {
            using (SqlDataReader reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    if (!reader.IsDBNull(0))
                    {
                        if (subjectCourseDict.ContainsKey(reader.GetString(1)))
                        {
                            subjectCourseDict[reader.GetString(1)].Add(reader.GetInt32(0));
                        }
                        else
                        {
                            List<int> courses = new List<int>();
                            courses.Add(reader.GetInt32(0));
                            subjectCourseDict.Add(reader.GetString(1), courses);
                        }
                    }
                }
            }
        }

        // create a list of course numbers of all open courses and all closed courses
        List<int> openCourses = new List<int>();
        List<int> fullCourses = new List<int>();

        // Loop through all subjects in subjectCourseDict
        foreach (KeyValuePair<string, List<int>> pair in subjectCourseDict)
        {
            // Check the open status of the courses in the subject
            List<Tuple<int, bool>> courseStatuses = CheckSubjectCourses(pair);

            // Loop through the course statuses
            foreach (Tuple<int, bool> courseStatus in courseStatuses)
            {
                // Add each course to the appropriate list depending on its status
                if (courseStatus.Item2)
                {
                    openCourses.Add(courseStatus.Item1);
                }
                else
                {
                    fullCourses.Add(courseStatus.Item1);
                }
            }
        }

        if (openCourses.Count > 0)
        {
            // Instead of running a command for each course in the list, create a string
            // of all the courses to search for and only iterate through the table once
            string openCoursesStr = BuildCoursesString(openCourses);

            // If a CourseNum is in the list of courses, then update the OpenStatus to 1 (now open)
            sql = $"Update Courses SET OpenStatus = 1 WHERE CourseNum IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }

            // Select the information needed to email the user if their subscribed course is open and
            // they are set to receive notifications
            sql = $@"SELECT Email, S.CourseNum, Title, Section FROM Subscriptions S
                    INNER JOIN Courses ON S.CourseNum = Courses.CourseNum
                    INNER JOIN Users ON Users.UserID = S.UserID
                    WHERE S.CourseNum IN {openCoursesStr} AND TrackStatus = 1";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1), reader.GetString(2), reader.GetString(3), apiKey).Wait();
                    }
                }
            }
            // Update TrackStatus to 0 for open course subscriptions
            sql = $"Update Subscriptions SET TrackStatus = 0 WHERE CourseNum IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }
        }

        if (fullCourses.Count > 0)
        {
            // Create the string for all full courses
            string fullCoursesStr = BuildCoursesString(fullCourses);

            // Set the OpenStatus for full courses to 0 and update the TrackStatus for all
            // users following those full courses back to 1
            sql = $@"UPDATE Courses SET OpenStatus = 0 WHERE CourseNum in {fullCoursesStr};
            UPDATE Subscriptions SET TrackStatus = 1 WHERE CourseNum IN {fullCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }
        }
    }
}

/*
 * Returns a parenthesized string of a given list of integers
 *
 * List<int> courseList: list of course numbers
 */
private static string BuildCoursesString(List<int> courseList)
{
    StringBuilder CoursesStrBldr = new StringBuilder("(");
    foreach (int courseNum in courseList)
    {
        CoursesStrBldr.Append(courseNum).Append(',');
    }
    CoursesStrBldr.Length--;
    CoursesStrBldr.Append(')');
    string coursesStr = CoursesStrBldr.ToString();
    return coursesStr;
}


/*
 * Given a SubjectCode and a list of courseNums to check, returns a list of tuples of course numbers and
 * the courses' open statuses.
 * ie. { (100, true), (101, false), (102, true), (103, true) }
 *
 * courses.Key: the subject code of the courses being checked. This is used to load the course roster page.
 * courses.Value: a list of all the course numbers being checked
 */
private static List<Tuple<int, bool>> CheckSubjectCourses(KeyValuePair<string, List<int>> courses)
{
    string url = $"http://classes.cornell.edu/browse/roster/FA17/subject/{courses.Key}";
    HtmlWeb htmlWeb = new HtmlWeb();
    HtmlDocument htmlDocument = htmlWeb.Load(url);
    HtmlNode[] courseNumNodes = htmlDocument.DocumentNode.SelectNodes("//strong").ToArray();

    List<Tuple<int, bool>> statuses = new List<Tuple<int, bool>>();
    foreach (HtmlNode courseNumNode in courseNumNodes)
    {
        int courseNum = int.Parse(Regex.Replace(courseNumNode.InnerHtml, @"\D", ""));
        if (courses.Value.Contains(courseNum))
        {
            string status = courseNumNode.ParentNode.ParentNode.ParentNode.SelectNodes(
                                        ".//i").First().Attributes["class"].Value;
            if (status.Contains("open-status-open"))
            {
                Tuple<int, bool> courseStatus = new Tuple<int, bool>(courseNum, true);
                statuses.Add(courseStatus);
            }
            else
            {
                Tuple<int, bool> courseStatus = new Tuple<int, bool>(courseNum, false);
                statuses.Add(courseStatus);
            }
        }
    }
    return statuses;
}


/*
 * Sends the notification email to the user.
 *
 * string email: email address of the user
 * int courseNum: course ID of the now open course
 * string title: the title of the course
 * string section: section information (ie. "LEC 001")
 * string apiKey: SendGrid API key
 */
private static async Task SendEmail(string email, int courseNum, string title, string section, string apiKey)
{
    dynamic sg = new SendGridAPIClient(apiKey);
    Email from = new Email("mailer@cornellcoursegrab.com");
    Email to = new Email(email);
    string subject = $"Course ID {courseNum}: {title}, {section} is now open!";
    string directory = System.Environment.CurrentDirectory;
    string message = System.IO.File.ReadAllText("D:\\home\\site\\wwwroot\\CourseGrabNotifier\\message.html");
    Content content = new Content("text/html", message);
    Mail mail = new Mail(from, subject, to, content);
    dynamic response = await sg.client.mail.send.post(requestBody: mail.Get());
}