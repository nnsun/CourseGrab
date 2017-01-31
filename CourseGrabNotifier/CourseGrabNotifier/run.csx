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
    string server = Environment.GetEnvironmentVariable("DB_SERVER");
    string database = Environment.GetEnvironmentVariable("DB_NAME");
    string username = Environment.GetEnvironmentVariable("DB_USERNAME");
    string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
    string apiKey = Environment.GetEnvironmentVariable("SENDGRID_API_KEY");

    string connectionString = $@"Server={server},1433;
                                Initial Catalog={database};Persist Security Info=False;
                                User ID={username};Password={password};MultipleActiveResultSets=False;
                                Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

    Dictionary<string, List<int>> subjectCourseDict = new Dictionary<string, List<int>>();
    using (SqlConnection connection = new SqlConnection(connectionString))
    {
        connection.Open();

        string sql = @"SELECT Subscription_1, Courses.SubjectCode FROM Users 
                        INNER JOIN Courses ON Users.Subscription_1 = Courses.CourseNum";
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



        sql = @"SELECT Subscription_2, Courses.SubjectCode FROM Users 
                INNER JOIN Courses ON Users.Subscription_2 = Courses.CourseNum";
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

        sql = @"SELECT Subscription_3, Courses.SubjectCode FROM Users 
            INNER JOIN Courses ON Users.Subscription_3 = Courses.CourseNum";
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

        List<int> openCourses = new List<int>();
        List<int> fullCourses = new List<int>();

        foreach (KeyValuePair<string, List<int>> pair in subjectCourseDict)
        {
            List<Tuple<int, bool>> courseStatuses = CheckSubjectCourses(pair);
            foreach (Tuple<int, bool> courseStatus in courseStatuses)
            {
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
            StringBuilder openCoursesStrBldr = new StringBuilder("(");
            foreach (int courseNum in openCourses)
            {
                openCoursesStrBldr.Append(courseNum).Append(',');
            }
            openCoursesStrBldr.Length--;
            openCoursesStrBldr.Append(')');
            string openCoursesStr = openCoursesStrBldr.ToString();

            sql = $"Update Courses SET CheckStatus = 1 WHERE CourseNum IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }

            sql = $"SELECT Email, Subscription_1 FROM Users WHERE Subscription_1 IN {openCoursesStr} AND TrackStatus_1 = 1";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1), apiKey).Wait();
                    }
                }
            }
            sql = $"Update Users SET TrackStatus_1 = 0 WHERE Subscription_1 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }

            sql = $"SELECT Email, Subscription_2 FROM Users WHERE Subscription_2 IN {openCoursesStr} AND TrackStatus_2 = 1";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1), apiKey).Wait();
                    }
                }
            }
            sql = $"Update Users SET TrackStatus_2 = 0 WHERE Subscription_2 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }

            sql = $"SELECT Email, Subscription_3 FROM Users WHERE Subscription_3 IN {openCoursesStr} AND TrackStatus_3 = 1";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1), apiKey).Wait();
                    }
                }
            }
            sql = $"Update Users SET TrackStatus_3 = 0 WHERE Subscription_3 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }
        }

        if (fullCourses.Count > 0)
        {
            StringBuilder fullCoursesStrBldr = new StringBuilder("(");
            foreach (int courseNum in fullCourses)
            {
                fullCoursesStrBldr.Append(courseNum).Append(',');
            }
            fullCoursesStrBldr.Length--;
            fullCoursesStrBldr.Append(')');
            string fullCoursesStr = fullCoursesStrBldr.ToString();

            sql = $@"UPDATE Courses SET CheckStatus = 0 WHERE CourseNum in {fullCoursesStr};
            UPDATE Users SET TrackStatus_1 = 1 WHERE Subscription_1 IN {fullCoursesStr};
            UPDATE Users SET TrackStatus_2 = 1 WHERE Subscription_2 IN {fullCoursesStr};
            UPDATE Users SET TrackStatus_3 = 1 WHERE Subscription_3 in {fullCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }
        }
    }
}


private static List<Tuple<int, bool>> CheckSubjectCourses(KeyValuePair<string, List<int>> courses)
{
    string url = $"http://classes.cornell.edu/browse/roster/SP17/subject/{courses.Key}";
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


private static async Task SendEmail(string email, int courseNum, string apiKey)
{
    dynamic sg = new SendGridAPIClient(apiKey);
    Email from = new Email("mailer@cornellcoursegrab.com");
    Email to = new Email(email);
    string subject = $"Course number {courseNum} is now open!";
    Content content = new Content("text/plain", "Go to studentcenter.cornell.edu to add it!");
    Mail mail = new Mail(from, subject, to, content);
    dynamic response = await sg.client.mail.send.post(requestBody: mail.Get());
}