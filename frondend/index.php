<?php
// yhteyden tietokantaan
include('C:\xampp\htdocs\CafeteriaMenuDisplay\frondend\data\connect_dp.php');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu</title>
    <style>
        body {
            background: #2c2c2c;
            color: white;
        }
        .lounas { width: 275px; height: 250px; float: left; padding: 10px; border: solid black 1px; font-size: 3vh;} 
        .ruuat { width: 275px; height: 150px; float: left; padding: 10px; border: solid black 1px; font-size: 3vh;} 
        .juomat { width: 275px; height: 100%; float: left; padding: 10px; margin: 0; border: solid black 1px; font-size: 3vh;} 
        .aikataulut { width: 145px; height: 75px; float: left; padding: 10px; border: solid black 1px; font-size: 3vh; }
</style>
</head>
<body>
    <!-- lounas -->
    <div id="1">
        <?php
        date_default_timezone_set("UTC");
        $sql = "SELECT ruoka, paivamaara, ainekset, juomat FROM viikonlounasRuokamenu";
        // Execute the SQL query
        $result = $conn->query($sql);
        // Process the result set
        if ($result->num_rows > 0) {
            // Output data of each row
            echo "<h1 style='text-align: center;'>Lounas menu</h1>";
            while($row = $result->fetch_assoc()) {
                echo "<div class='lounas'>";
                echo $row["paivamaara"] . " ". date("l", strtotime($row["paivamaara"])) ."<br>";
                echo "<br/>";    

                echo "Ruoka:" . "<br>";
                echo $row["ruoka"]. "<br>";
                echo "<br/>";    

                echo "Ainekset:" . "<br>";
                echo $row["ainekset"]. "<br>";
                echo "<br/>";    
                echo "Juoma vaihtoehdot:" . "<br>";
                echo  $row["juomat"]. "<br>";
                echo "</div>";
            }
        } else {
            echo "0 results";
        }
        ?>
    </div>
    <!-- ruuat -->
    <div id="2" style="display: none;">
        <?php
        $sql = "SELECT ruokalaji, ruoka, ainekset, hinta FROM ruokamenu";
        // Execute the SQL query
        $result = $conn->query($sql);
        // Process the result set
        if ($result->num_rows > 0) {
            echo "<h1 style='text-align: center;'>Ruokalista</h1>";
            // Output data of each row
            while($row = $result->fetch_assoc()) {
                echo "<div class='ruuat'>";

                echo  $row["ruoka"]. "<br>";
                echo "<br/>";    

                echo "Ainekset:" . "<br>";
                echo $row["ainekset"]. "<br>";
                echo "<br/>";    

                echo "hinta:" . "<br>";
                echo $row["hinta"].' €'. "<br>";
                echo "<br/>";    

                echo "</div>";
            }
        } else {
            echo "0 results";
        }
        ?>
    </div>
    <!-- juomat -->
    <div id="3" style="display: none;">
        <?php
        $sql = "SELECT juoma, hinta FROM juomat WHERE tyyppi='kuumajuoma'";
        // Execute the SQL query
        $result = $conn->query($sql);
        // Process the result set
        echo "<div style='display: flex; flex-direction: row;'>";
        echo "<h1>Kuumatjuomat</h1> "." <h1 style='padding-left: 90px;'>Kylmätjuomat</h1>";
        echo "</div>";
        if ($result->num_rows > 0) {
            // Output data of each row
            echo "<div class='juomat'>";
            while($row = $result->fetch_assoc()) {
                echo "<br/>";    
                echo $row["juoma"]. " " . $row["hinta"] .' €'. "<br>";
                echo "<br/>";    
            }
            echo "</div>";
        } else {
            echo "0 results";
        }
        ?>
        <?php
        $sql = "SELECT juoma, hinta FROM juomat WHERE tyyppi='kylmajuoma'";
        // Execute the SQL query
        $result = $conn->query($sql);
        // Process the result set
        if ($result->num_rows > 0) {
            // Output data of each row
            echo "<div class='juomat'>";
            while($row = $result->fetch_assoc()) {
                echo "<br/>";    
                echo $row["juoma"]. " " . $row["hinta"] .' €' . "<br>";
                echo "<br/>";    
            }
            echo "</div>";
        } else {
            echo "0 results";
        }
        ?>
    </div>
    <!-- aukioloajat -->
    <div id="4" style="display: none;">
        <?php
        $sql = "SELECT paiva, kellonaika, paivamaara FROM aukioloajat";
        // Execute the SQL query
        $result = $conn->query($sql);
        // Process the result set
        if ($result->num_rows > 0) {
            // Output data of each row
            echo "<h1 style='text-align: center;'>Aukioloajat</h1>";
            while($row = $result->fetch_assoc()) {
                echo "<div class='aikataulut'>";
                echo $row["paiva"]. " " . $row["kellonaika"] . "<br>";   
                echo "<br/>";
                echo date("l", strtotime($row["paivamaara"]));   
                echo "</div>";
            }
        } else {
            echo "0 results";
        }
        ?>
    </div>
    <script>
        // does the dia show
        let ikkuna = 2
        function display() {
            switch (ikkuna) {
                case 2:
                    console.log("vaihot")
                    document.getElementById("4").style.display = "none"
                    document.getElementById("1").style.display = "none"
                    document.getElementById("2").style.display = "block"
                    break;
                case 3:
                    document.getElementById("1").style.display = "none"
                    document.getElementById("2").style.display = "none"
                    document.getElementById("3").style.display = "block"
                    break;
                case 4:
                    document.getElementById("1").style.display = "none"
                    document.getElementById("2").style.display = "none"
                    document.getElementById("3").style.display = "none"
                    document.getElementById("4").style.display = "block"
                    break;
                case 5:
                    document.getElementById("1").style.display = "block"
                    document.getElementById("2").style.display = "none"
                    document.getElementById("3").style.display = "none"
                    document.getElementById("4").style.display = "none"
                    ikkuna = 1
            }
            ikkuna += 1
        }
        setInterval(display, 10000);
    </script>
</body>
</html>

