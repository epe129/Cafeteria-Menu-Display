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
            margin: 0;
            padding: 20px;
            background: #f3f4f6;
            color: #1f2937;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }

        h1 {
            text-align: center;
            color: #111827;
            font-size: 2.3rem;
        }

        .lounas,
        .ruuat,
        .juomat,
        .aikataulut {
            float: left;
            width: 260px;
            padding: 16px;
            margin: 10px;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            background: #ffffff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            font-size: 1.20rem;
            line-height: 1.6;
            color: #1f2937;
        }

        .lounas {
            max-height: 380px;
        }

        .ruuat {
            min-height: 240px;
        }

        .juomat {
            min-height: 200px;
        }

        .aikataulut {
            min-height: 75px;
        }
    </style>
</head>
<body>
    <!-- lounas -->
    <div id="1">
        <?php
        $countLunch = 0;
        date_default_timezone_set("UTC");
        $sql = "SELECT ruoka, paivamaara, ainekset, juomat FROM viikonlounasRuokamenu";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            echo "<h1 style='text-align: center;'>Lounas menu</h1>";
            while($row = $result->fetch_assoc()) {
                if ($row["paivamaara"] >= date("Y-m-d")) {
                    $countLunch += 1;
                    echo "<div class='lounas'>";
                    echo "<h3>".date("l", strtotime($row["paivamaara"])). "</h3>";
                    echo "<h3>".date('d.m.Y', strtotime($row["paivamaara"])) . "</h3>";

                    echo "<h3>".$row["ruoka"]. "</h3>";

                    echo "Ainekset:" . "<br>";
                    echo $row["ainekset"]. "<br>";
                    echo "<br/>";    
                    echo "Juoma vaihtoehdot:" . "<br>";
                    echo  $row["juomat"]. "<br>";
                    echo "</div>";
                    if ($countLunch == 7) { break; }
                }
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
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            echo "<h1 style='text-align: center;'>Ruokalista</h1>";
            while($row = $result->fetch_assoc()) {
                echo "<div class='ruuat'>";

                echo "<h3>". $row["ruoka"]. "</h3>";

                echo "Ainekset:" . "<br>";
                echo $row["ainekset"]. "<br>";
                echo "<br/>";    

                echo "hinta:" . "<br>";
                echo $row["hinta"].' €'. "<br>";
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
        $result = $conn->query($sql);
        echo "<div style='width: 60%; margin-left: auto; margin-right: auto;'>";
        if ($result->num_rows > 0) {
            echo "<div style='float: left;'>";
            echo "<h1>Kuumatjuomat</h1>";
            echo "<div class='juomat' style='float: left;'>";
            while($row = $result->fetch_assoc()) {
                echo "<p style='font-size: 1.8rem;'>".  $row["juoma"]. " " . $row["hinta"] .' €'. "</p>";
            }
            echo "</div>";
            echo "</div>";
        } else {
            echo "0 results";
        }
        ?>
        <?php
        $sql = "SELECT juoma, hinta FROM juomat WHERE tyyppi='kylmajuoma'";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            echo "<div style='float: right;'>";
            echo "<h1>Kylmätjuomat</h1>";
            echo "<div class='juomat' style='float: right;'>";
            while($row = $result->fetch_assoc()) {
                echo "<p style='font-size: 1.8rem;'>". $row["juoma"]. " " . $row["hinta"] .' €' . "</p>";
            }
            echo "</div>";
            echo "</div>";

        } else {
            echo "0 results";
        }
        echo "</div>";
        ?>
    </div>
    <!-- aukioloajat -->
    <div id="4" style="display: none;">
        <?php
        $sql = "SELECT paiva, kellonaika, paivamaara FROM aukioloajat";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            echo "<h1 style='text-align: center;'>Aukioloajat</h1>";
            while($row = $result->fetch_assoc()) {
                if ($row["paivamaara"] >= date("Y-m-d")) {
                    echo "<div class='aikataulut'>";
                    echo "<p style='font-size: 1.8rem; font-weight: 700;'>". $row["paiva"]. " " . $row["kellonaika"] . "</p>";   
                    echo  "<p style='font-size: 1.8rem; font-weight: 600;'>". date('d.m.Y', strtotime($row["paivamaara"])) . "</p>";   
                    echo "</div>";
                }
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
        
        // reloads the pages every 50 seconds so if some thing changes it updates to the page 
        function relo() {
            location.reload()
        }
        setInterval(relo, 50000);
    </script>
</body>
</html>

