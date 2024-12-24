import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
def get_user_list():
    """
    Kết nối đến cơ sở dữ liệu MySQL và trả về danh sách user dưới dạng DataFrame.
    """
    try:
        # Kết nối đến MySQL
        connection = mysql.connector.connect(
            host='172.16.1.7',  # Thay bằng thông tin của bạn
            database='jwdb',   # Tên database
            user='root',       # Tên user
            password='Xv3w8y9r0kMJH6q3zRnnUR' # Mật khẩu
        )

        if connection.is_connected():

            query = """
            SELECT
    username as "Tổng đài viên",
    de.employeeCode as "Số nội bộ",
    c_statusName as "Trạng thái",
    de.departmentId AS "Nhóm",
    TIME_FORMAT(TIMEDIFF(NOW(), c_dateStatusChanged),'%H:%i:%s') AS "Thời gian"
FROM
    jwdb.app_fd_User au
JOIN
    jwdb.dir_user du ON au.id = du.id
JOIN
    jwdb.dir_employment de ON de.userId = du.id
where coalesce(c_statusName,'Logout')<>'Logout'
ORDER BY
    CASE c_statusName
        WHEN 'No ACD' THEN 1
        WHEN 'Available' THEN 2
        WHEN 'Callback' THEN 3
        WHEN 'Campaign' THEN 4
        WHEN 'Outbound' THEN 5
        WHEN 'Lunch' THEN 6
        WHEN 'Meeting' THEN 7
        ELSE 8
    END;
            """

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()

            # Chuyển đổi kết quả thành DataFrame
            df = pd.DataFrame(result)
            #print(f"get_user_list {datetime.now()}")
            return df

    except Error as e:
        return pd.DataFrame()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def get_group_list():
    """
    Kết nối đến cơ sở dữ liệu MySQL và trả về danh sách user dưới dạng DataFrame.
    """
    try:
        # Kết nối đến MySQL
        connection = mysql.connector.connect(
            host='172.16.1.7',  # Thay bằng thông tin của bạn
            database='jwdb',   # Tên database
            user='root',       # Tên user
            password='Xv3w8y9r0kMJH6q3zRnnUR' # Mật khẩu
        )

        if connection.is_connected():

            query = """
             WITH roles AS (
                    SELECT 'LPBank' AS role
                    UNION ALL
                    SELECT 'OKC' AS role
                    UNION ALL
                    SELECT 'OMP' AS role
                )
                SELECT
                    r.role as "Group",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'No ACD' THEN 1 ELSE 0 END), 0) AS "No ACD",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Available' THEN 1 ELSE 0 END), 0) AS "Available",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Meeting' THEN 1 ELSE 0 END), 0) AS "Meeting",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Logout' THEN 1 ELSE 0 END), 0) AS "Logout",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Lunch' THEN 1 ELSE 0 END), 0) AS "Lunch",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Callback' THEN 1 ELSE 0 END), 0) AS "Callback",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Outbound' THEN 1 ELSE 0 END), 0) AS "Outbound",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Campaign' THEN 1 ELSE 0 END), 0) AS "Campaign"
                FROM
                    roles r
                LEFT JOIN
                    jwdb.app_fd_User a ON a.c_groups = r.role AND COALESCE(a.c_groups, '') <> ''
                LEFT JOIN
                    jwdb.dir_employment e ON a.id = e.userId AND COALESCE(e.employeeCode, '') <> ''
                GROUP BY
                    r.role
                UNION ALL
                select "Tổng" as "Group",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'No ACD' THEN 1 ELSE 0 END), 0) AS "No ACD",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Available' THEN 1 ELSE 0 END), 0) AS "Available",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Meeting' THEN 1 ELSE 0 END), 0) AS "Meeting",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Logout' THEN 1 ELSE 0 END), 0) AS "Logout",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Lunch' THEN 1 ELSE 0 END), 0) AS "Lunch",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Callback' THEN 1 ELSE 0 END), 0) AS "Callback",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Outbound' THEN 1 ELSE 0 END), 0) AS "Outbound",
                    COALESCE(SUM(CASE WHEN a.c_statusName = 'Campaign' THEN 1 ELSE 0 END), 0) AS "Campaign"
                FROM
                    roles r
                LEFT JOIN
                    jwdb.app_fd_User a ON a.c_groups = r.role AND COALESCE(a.c_groups, '') <> ''
                LEFT JOIN
                    jwdb.dir_employment e ON a.id = e.userId AND COALESCE(e.employeeCode, '') <> '';
            """

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()

            # Chuyển đổi kết quả thành DataFrame
            df = pd.DataFrame(result)
            return df

    except Error as e:
        return pd.DataFrame()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_ongoing_3cx():
    """
    Kết nối đến cơ sở dữ liệu MySQL và trả về danh sách user dưới dạng DataFrame.
    """
    try:
        # Kết nối đến MySQL
        connection = mysql.connector.connect(
            host='172.16.1.7',  # Thay bằng thông tin của bạn
            database='jwdb',   # Tên database
            user='root',       # Tên user
            password='Xv3w8y9r0kMJH6q3zRnnUR' # Mật khẩu
        )

        if connection.is_connected():

            query = """
             select c_Type as "Hướng",
       c_LastChangeStatus as "Thời gian",
       c_customer_phone as "SĐT",
       c_customer_name as "KH",
       c_customer_rank as "Hạng KH",
       c_agent_name as "Agent",
       TIME_FORMAT(TIMEDIFF(NOW(), c_LastChangeStatus),'%H:%i:%s') as "Thời lượng",
       c_Queue as "Nhánh L3 IVR"
from jwdb.app_fd_3cx_call
where c_Status="Talking";
            """

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()

            # Chuyển đổi kết quả thành DataFrame
            df = pd.DataFrame(result)

            return df

    except Error as e:
        return pd.DataFrame()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def get_waiting_3cx():
    """
    Kết nối đến cơ sở dữ liệu MySQL và trả về danh sách user dưới dạng DataFrame.
    """
    try:
        # Kết nối đến MySQL
        connection = mysql.connector.connect(
            host='172.16.1.7',  # Thay bằng thông tin của bạn
            database='jwdb',   # Tên database
            user='root',       # Tên user
            password='Xv3w8y9r0kMJH6q3zRnnUR' # Mật khẩu
        )

        if connection.is_connected():

            query = """
             select c_Type as "Hướng",
       c_LastChangeStatus as "Thời gian",
       c_customer_phone as "SĐT",
       c_customer_name as "KH",
       c_customer_rank as "Hạng KH",
       c_agent_name as "Agent",
       TIME_FORMAT(TIMEDIFF(NOW(), c_LastChangeStatus),'%H:%i:%s') as "Thời lượng",
       c_Queue as "Nhánh L3 IVR"
from jwdb.app_fd_3cx_call
where c_Status<>"Talking";
            """

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()

            # Chuyển đổi kết quả thành DataFrame
            df = pd.DataFrame(result)

            return df

    except Error as e:
        return pd.DataFrame()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()