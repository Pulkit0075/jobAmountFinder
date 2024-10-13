<?php
// login.php

// Database connection details
$servername = "localhost"; // Change if your DB is hosted elsewhere
$db_username = "root";     // Your database username
$db_password = "";         // Your database password
$dbname = "joblist";       // Your database name

// Create a connection to the database
$conn = new mysqli($servername, $db_username, $db_password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Enable error reporting for SQL
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get email and password from the POST request
    $email = htmlspecialchars($_POST['e']);
    $pass = htmlspecialchars($_POST['p']);
    
    // Check if the user exists in the database
    $sql = "SELECT * FROM login WHERE Email = ?";
    
    if (!$stmt = $conn->prepare($sql)) {
        die("Error in SQL query: " . $conn->error); // Debug for query preparation
    }
    
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        // If user exists, check the password
        $row = $result->fetch_assoc();
        if ($pass === $row['Password']) {
            // Set cookies with a 1-hour expiration
            setcookie("user_id", $row['id'], time() + 3600, "/"); // Cookie expires in 1 hour
            setcookie("user_email", $row['Email'], time() + 3600, "/"); // Cookie expires in 1 hour

            // Redirect to option.html
            header("Location: option.html");
            exit();
        } else {
            // Incorrect password, redirect to wrongPassword.html
            header("Location: wrongPass.html");
            exit();
        }
    } else {
        // If user does not exist, create a new entry
        $insert_sql = "INSERT INTO login (Email, password) VALUES (?, ?)";
        if (!$insert_stmt = $conn->prepare($insert_sql)) {
            die("Error in SQL query: " . $conn->error); // Debug for insert query
        }
        
        $insert_stmt->bind_param("ss", $email, $pass);

        if ($insert_stmt->execute()) {
            // Retrieve the new user's ID
            $user_id = $insert_stmt->insert_id;

            // Set cookies with a 1-hour expiration
            setcookie("user_id", $user_id, time() + 3600, "/"); // Cookie expires in 1 hour
            setcookie("user_email", $email, time() + 3600, "/"); // Cookie expires in 1 hour

            // Redirect to option.html
            header("Location: option.html");
            exit();
        } else {
            echo "Error: " . $insert_stmt->error;
        }
    }

    // Close the prepared statements
    $stmt->close();
    $insert_stmt->close();
}

// Close the database connection
$conn->close();
?>
