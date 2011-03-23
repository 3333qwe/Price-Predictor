<?php

require_once dirname(__file__) . "/parse.php";
require_once dirname(__file__) . "/predict.php";

$users     = parse_csv("anonwhipdata.csv");
$predictor = new Predictor($users);

$sqdiff  = 0;
$matches = 0;
$sqcount = 0;

foreach ($users as $user) {
    if ($user->monthly_rate) {
        $predictor = new Predictor($users);
        $result    = $predictor->predict($user);
        if ($result) {
            $difference = $user->monthly_rate - $result->monthly_rate;
            $sqdiff  += $difference * $difference;
            $sqcount += 1;
            $matches += $result->matches;
        }
    }
}
printf("%0.2f   %0.2f\n", sqrt($sqdiff / $sqcount), ($matches / $sqcount));
