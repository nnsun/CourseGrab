#r "System.Configuration"
#r "System.Data"

using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Threading.Tasks;

public static void Run(TimerInfo myTimer, TraceWriter log)
{
    string connectionString = @"Server=tcp:coursegrabdb.database.windows.net,1433;
                            Initial Catalog=CourseGrabDB;Persist Security Info=False;
                            User ID=nnsun;Password=zDVfYZg7n3lC4TlaHPir;MultipleActiveResultSets=False;
                            Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";
    using (SqlConnection conn = new SqlConnection(connectionString))
    {
        conn.Open();
        string query = "SELECT TOP 50 * FROM Users";
        SqlCommand command = new SqlCommand(query, conn);
        SqlDataReader reader = command.ExecuteReader();
        while (reader.Read())
        {
            
        }
    }
}