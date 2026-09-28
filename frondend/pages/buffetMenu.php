<?php
// yhteyden tietokantaan
include('C:\xampp\htdocs\CafeteriaMenuDisplay\frondend\data\connect_dp.php');

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        div {
            height: 100%;
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: center; 
            align-items: center; 
        }
        div div { width: 33%; height: 100%;}
    </style>
</head>
<body>
    <div>
        <?php
        date_default_timezone_set("UTC");
        $sql = "SELECT ruoka, paivamaara, ainekset, juomat FROM viikonbuffetruokamenu";
        // Execute the SQL query
        $result = $conn->query($sql);
        // Process the result set
        if ($result->num_rows > 0) {
        // Output data of each row
        while($row = $result->fetch_assoc()) {
            echo "<div>";
            echo $row["paivamaara"] . " ". date("l", strtotime($row["paivamaara"])) ."<br>";
            echo "Ruoka:" . "<br>";
 
            echo $row["ruoka"]. "<br>";
            echo "Ainekset:" . "<br>";
 
            echo $row["ainekset"]. "<br>";
            echo "Juoma vaihtoehdot:" . "<br>";
 
            echo  $row["juomat"]. "<br>";
            echo "</div>";
        }
        } else {
        echo "0 results";
        }
        $conn->close();
        ?>
    </div>
</body>
</html>