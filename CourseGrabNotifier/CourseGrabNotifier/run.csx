#r "System.Configuration"
#r "System.Data"

using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Diagnostics;
using System.Text.RegularExpressions;
using HtmlAgilityPack;


public static void Run(TimerInfo myTimer, TraceWriter log)
{
    Stopwatch clock = Stopwatch.StartNew();

    string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
    string connectionString = $@"Server=tcp:coursegrabdb.database.windows.net,1433;
                                Initial Catalog=CourseGrabDB;Persist Security Info=False;
                                User ID=nnsun;Password={password};MultipleActiveResultSets=False;
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
            List<bool> courseStatuses = CheckSubjectCourses(pair, log);
            for (int i = 0; i < courseStatuses.Count; i++)
            {
                if (courseStatuses[i])
                {
                    openCourses.Add(pair.Value[i]);
                }
                else
                {
                    fullCourses.Add(pair.Value[i]);
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

            sql = $"SELECT Email, Subscription_1 FROM Users WHERE Subscription_1 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1));
                    }
                }
            }
            sql = $"Update Users SET TrackStatus_1 = 0 WHERE Subscription_1 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }

            sql = $"SELECT Email, Subscription_2 FROM Users WHERE Subscription_2 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1));
                    }
                }
            }
            sql = $"Update Users SET TrackStatus_2 = 0 WHERE Subscription_2 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }

            sql = $"SELECT Email, Subscription_3 FROM Users WHERE Subscription_3 IN {openCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        SendEmail(reader.GetString(0), reader.GetInt32(1));
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
            UPDATE Users SET TraackStatus_3 = 1 WHERE Subscription_3 in {fullCoursesStr}";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                command.ExecuteNonQuery();
            }
        }

        clock.Stop();
        log.Info($"Program took {clock.ElapsedMilliseconds} ms to execute");
    }
}


public static List<bool> CheckSubjectCourses(KeyValuePair<string, List<int>> courses, TraceWriter log)
{
    string url = $"http://classes.cornell.edu/browse/roster/SP17/subject/{courses.Key}";
    HtmlWeb htmlWeb = new HtmlWeb();
    HtmlDocument htmlDocument = htmlWeb.Load(url);
    HtmlNode[] courseNumNodes = htmlDocument.DocumentNode.SelectNodes("//strong").Where(
                                    x => x.Attributes.Contains("class") && 
                                    x.Attributes["class"].Value == "tooltip-iws" &&
                                    courses.Value.Contains(
                                        int.Parse(
                                            Regex.Replace(x.InnerHtml, @"\D", "")))).ToArray();

    log.Info(courseNumNodes.Count().ToString());
    //foreach (HtmlNode node in courseNumNodes)
    //{
    //    string r = Regex.Replace(node.InnerHtml, @"\D", "");
    //    log.Info(r);
    //}

    List<bool> courseStatuses = new List<bool>();
    foreach (int courseNum in courses.Value)
    {
        //HtmlNode node = courseNumNode.Where(x => x.InnerHtml == courseNum.ToString()).First();
    }


    return courseStatuses;
}


public static void SendEmail(string email, int courseNum)
{

}