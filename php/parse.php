<?php
require_once dirname(__file__) . "/model.php";

function parse_csv($filename) {
    $path   = realpath(dirname(__file__) . "/../data/" . $filename);
    $handle = fopen($path, "r");
    if ($handle === false) throw new Exception("Invalid file " . $filename);
    $first  = true;
    $users  = new UserCollection();
    while (($row = fgetcsv($handle)) !== false) {
        if ($first) {
            $first = false;
        } else {
            $fields = array();
            $fields['user_id']          = $row[0];
            $fields['status']           = $row[1];
            $fields['join_date']        = DateTime::createFromFormat("d/m/y", $row[2]);
            $fields['bookings']         = intval($row[3]);
            $fields['revenue']          = floatval($row[4]);
            $fields['location']         = strtolower($row[5]);
            $fields['reg_date']         = DateTime::createFromFormat("d/m/y", $row[6]);
            $fields['manufacture_date'] = DateTime::createFromFormat("d/m/y", $row[7]);
            $fields['make']             = $row[8];
            $fields['model']            = $row[9];
            $fields['colour']           = $row[10];
            list($fields['type'], $fields['doors'])  = _parse_type($row[11], $row[12]);
            $fields['seats']            = _parse_seats($row[13]);
            $fields['engine_cc']        = _parse_engine_cc($row[14]);
            $fields['engine_co2']       = _parse_engine_co2($row[15]);
            $fields['fuel']             = _parse_fuel($row[16]);
            $fields['transmission']     = _parse_transmission($row[17]);
            $fields['insurance_group']  = $row[18];
            $fields['hourly_rate']      = _parse_rate($row[19]);
            $fields['daily_rate']       = _parse_rate($row[20]);
            $fields['weekly_rate']      = _parse_rate($row[21]);
            $fields['monthly_rate']     = _parse_rate($row[22]);
            $fields['has_photos']       = strtolower($row[23]) == "yes";
            
            $users[] = new User($fields);
        }
    }
    return $users;
}

function _parse_type($v1, $v2) {
    $v1 = strtolower($v1);
    $v2 = strtolower($v2);
    $cartype = $v2;
    if (preg_match("#(hatchback|mpv|estate|saloon|convertible|coupe)#", $v1, $match)) {
        $cartype = $cartype . "." . $match[1];
    }
    $doors = preg_match("#(\d) door#", $v1, $match) ? $match[1] : null;
    
    return array($cartype, $doors);
}

function _parse_seats($value) {
    if (preg_match("#(\d+)(?: seats?)#", strtolower($value), $match)) {
        return intval($match[1]);
    } elseif ($value == "five comfortably") {
        return 5;
    } elseif ($value) {
        return intval($value);
    }
}

function _parse_engine_cc($value) {
    if (preg_match("#(\d+(?:\.\d+)) litres?#", $value, $match)) {
        return intval(floatval($match[1]) * 1000);
    } elseif (is_numeric($value)) {
        return intval($value);
    }
}

function _parse_engine_co2($value) {
    return intval($value);
}

function _parse_fuel($value) {
    $value = strtolower($value);
    return in_array($value, array("heavy-oil")) ? "diesel" : $value;
}

function _parse_transmission($value) {
    if ($value) {
        $value = strtolower($value);
        if (in_array($value, array("automatic", "cvt", "manual"))) {
            return $value;
        } elseif ($value == "tiptronic") {
            return "automatic.tiptronic";
        } else {
            return "unknown";
        }
    }
}

function _parse_rate($value) {
    return $value ? intval($value) : null;
}

echo parse_csv("anonwhipdata.csv");
echo "\n";