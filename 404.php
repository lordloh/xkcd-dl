<!doctype html>
<html>
    <head>
        <title>File not found - 404</title>
        <style type="text/css">
            .center{
                text-align:center;
            }
            .caption{
                font-style:italic;
                font-size:1.8em;
                font-family:calibri;
            }
            .imgTitle{
                font-weight:bold;
                font-size:2em;
                font-family:calibri;
            }
            .heading404{
                font-size:3em;
                font-family:calibri;
            }
        </style>
    </head>
    <body>
        <h1 class="center heading404">404</h1>
        <hr/>
        <?php
            function dbg($data){
                echo"<pre>";
                print_r($data);
                echo "</pre>";
            }
            $json_file=file_get_contents("xkcd_archive/meta/meta.json");
            $comic_meta=json_decode($json_file);
            $comic_number=rand(0,count($comic_meta));
            $comic=$comic_meta[$comic_number];
            echo "<div class='center'><h2 class='imgTitle'>".$comic->title."</h2>
                <img src='$comic->img' alt='$comic->alt' /><br/>"
                ."<span class='caption'>".$comic->alt."</span></div>";
        ?>
    </body>
</html>
    