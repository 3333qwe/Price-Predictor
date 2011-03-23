<?php

class Predictor
{
    private $_users;

    function __construct(UserCollection $users) {
        $this->_users = clone($users);
    }

    public function predict($user)
    {
        $monthly_rate  = 0;
        $matches = 0;
        $this->_users = $this->_users->remove($user);
        foreach ($this->_users as $u) {
            if ($u->bookings && $u->monthly_rate != null) {
                if (abs($u->reg_date->getTimestamp() - $user->reg_date->getTimestamp()) < (2 * 365 * 86400)) {
                    if (abs($u->insurance_group - $user->insurance_group) < 3) {
                        $monthly_rate += $u->monthly_rate;
                        $matches++;
                    }
                }
            }
        }
        return $matches ? new Result($monthly_rate / $matches, $matches) : null;
    }
}

class Result
{
    public $monthly_rate, $matches;

    public function __construct($monthly_rate, $matches) {
        $this->monthly_rate  = $monthly_rate;
        $this->matches       = $matches;
    }
}