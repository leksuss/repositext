
function local_settings {
    if [ "$OPTS" == "" ]
    then
        local_settings=$(cat local.py | grep project_settings | cut -d "=" -f2 | xargs)
        if [ "$local_settings" == "" ]
        then 
            break
        else
            OPTS="--settings $local_settings"
        fi
    fi
    echo $OPTS
}
