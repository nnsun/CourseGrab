#r "System.Configuration"
#r "System.Data"

using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Threading.Tasks;

public static void Run(TimerInfo myTimer, TraceWriter log)
{
    string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
    string connectionString = $@"Server=tcp:coursegrabdb.database.windows.net,1433;
                            Initial Catalog=CourseGrabDB;Persist Security Info=False;
                            User ID=nnsun;Password={password};MultipleActiveResultSets=False;
                            Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";

    using (SqlConnection connection = new SqlConnection(connectionString))
    {
        connection.Open();
        string query = "SELECT TOP 50 * FROM Users";
        SqlCommand command = new SqlCommand(query, connection);
        SqlDataReader reader = command.ExecuteReader();
        while (reader.Read())
        {

        }
    }
}