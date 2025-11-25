#/!/bin/bash
# post_uninstall script for mate-tweak: reset the window manager
# This will fix: After changing windowmanager and uninstall mate-tweak, you are maybe without any window-manager in mate.

while read user; do
    #has dconf?
    sudo -u "$user" -H -s eval 'ls $HOME/.config/dconf 2>> /dev/null > /dev/null'
    if [ "${?}" -eq "0" ]
    then
        wm=$(sudo -u "$user" -H gsettings get org.mate.session.required-components windowmanager | sed s/\'//g)
        # echo $wm
        if [ "$wm" = "marco-compton" ] || 
           [ "$wm" = "marco-glx" ] ||
           [ "$wm" = "marco-no-composite" ] || 
           [ "$wm" = "marco-picom" ] || 
           [ "$wm" = "marco-xrender" ] || 
           [ "$wm" = "marco-xr_glx_hybrid" ]
          then
              echo "Reset to default window-manager ('marco') for user $user , because $wm was removed."
              echo $(sudo -u "$user" -H dbus-run-session gsettings reset org.mate.session.required-components windowmanager)
              # echo $(sudo -u "$user" -H gsettings get org.mate.session.required-components windowmanager)
        fi
    fi
done < <(getent passwd | awk -F ':' '$3>=1000 {print $1}')
