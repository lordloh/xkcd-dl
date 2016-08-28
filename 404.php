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
            footer{
                font-size:small;
                font-family:'courier New', Courier;
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
            if (file_exists("timefile")){
                $time_file_contents=file_get_contents("timefile");
                $time_part=explode("*",$time_file_contents);
                if(time()-$time_part[0]>600){
                    $r=file_put_contents("timefile",time()."*".$comic_number);
                }else{
                    if (count($time_part>1)) $comic_number=$time_part[1];
                }
            }else{
                file_put_contents("timefile",time()."*".$comic_number);
            }
            $comic=$comic_meta[$comic_number];
            echo "<div class=\"center\"><h2 class=\"imgTitle\">".$comic->title."</h2>
                <img src=\"".$_SERVER['CONTEXT_PREFIX'].$comic->img."\" alt=\"$comic->alt\" /><br/>"
                ."<span class=\"caption\">".$comic->alt."</span></div>";
        ?>
        <hr/>
        <footer><a href="https://xkcd.com/">xkcd comics</a> are licensed under a Creative Commons Attribution-NonCommercial 2.5 License<br/>Get the source code of the <a href="https://github.com/lordloh/xkcd-dl">xkcd 404 pages on github</a>.</footer>
    </body>
</html>
    