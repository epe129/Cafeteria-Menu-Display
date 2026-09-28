<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu</title>
</head>
<body>
    <!-- pages are shown in the dia show -->
    <div id="1">
        <?php
        include './pages/buffetMenu.php';
        ?>
    </div>
    <div id="2" style="display: none;">
        <?php
        include './pages/foodsMenu.php';
        ?>
    </div>
    <div id="3" style="display: none;">
        <?php
        include './pages/drinksMenu.php';
        ?>
    </div>
    <div id="4" style="display: none;">
        <?php
        include './pages/openHours.php';
        ?>
    </div>
    <script>
        // does the dia show
        let ikkuna = 2
        function display() {
            switch (ikkuna) {
                case 2:
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

