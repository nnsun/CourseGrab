#r "System.Configuration"
#r "System.Data"

using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Diagnostics;


public static void Run(TimerInfo myTimer, TraceWriter log)
{
    Stopwatch clock = Stopwatch.StartNew();

    string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
    string connectionString = $@"Server=tcp:coursegrabdb.database.windows.net,1433;
                            Initial Catalog=CourseGrabDB;Persist Security Info=False;
                            User ID=nnsun;Password={password};MultipleActiveResultSets=False;
                            Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

    HashSet<int> trackedCourses = new HashSet<int>();

    using (SqlConnection connection = new SqlConnection(connectionString))
    {
        connection.Open();


        string query = "SELECT DISTINCT Subscription_1 FROM Users";
        using (SqlCommand command = new SqlCommand(query, connection))
        {
            using (SqlDataReader reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    if (!reader.IsDBNull(0))
                    {
                        trackedCourses.Add(reader.GetInt32(0));
                    }
                }
            }
        }

        query = "SELECT DISTINCT Subscription_2 FROM Users";
        using (SqlCommand command = new SqlCommand(query, connection))
        {
            using (SqlDataReader reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    if (!reader.IsDBNull(0))
                    {
                        trackedCourses.Add(reader.GetInt32(0));
                    }
                }
            }
        }

        query = "SELECT DISTINCT Subscription_3 FROM Users";
        using (SqlCommand command = new SqlCommand(query, connection))
        {
            using (SqlDataReader reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    if (!reader.IsDBNull(0))
                    {
                        trackedCourses.Add(reader.GetInt32(0));
                    }
                }
            }
        }




        clock.Stop();
        log.Info($"Program took {clock.ElapsedMilliseconds} ms to execute");
    }
}