<?php

class User
{
    private $_fields = array();

    public function __construct($fields)
    {
        $this->_fields = $fields;
    }

    public function __get($name) {
        if (!array_key_exists($name, $this->_fields)) {
            throw new Exception("Invalid property access $name.");
        }
        return $this->_fields[$name];
    }

    public function equals($other) {
        return $this->user_id == $other->user_id;
    }

    public function __toString() {
        return $this->user_id;
    }
}

class UserCollection extends ArrayObject
{
    function remove($user) {
        $collection = new UserCollection();
        foreach ($this as $u) {
            if ($u->user_id != $user->user_id) {
                $collection[] = $u;
            }
        }
        return $collection;
    }

    function __toString() {
        return "" . count($this);
    }
}