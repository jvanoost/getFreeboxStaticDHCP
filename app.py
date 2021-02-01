from cFreebox import *

maFreebox = cFreebox()

##############################################
def menu():
    global maFreebox

    print('')
    print('1. Sauvegarder mes IP statiques')
    print('2. Charger mes IP statiques sur ma Freebox')
    print('3. Sauvegarder mes redirections de ports')
    print('4. Sauvegarder mes redirections de ports sur ma Freebox')
    print('5. Sauvegarder mes Wifi guest')
    print('6. Sauvegarder mes Wifi guest sur ma Freebox')
    print('7. Sauvegarder mes MAC filter')
    print('8. Sauvegarder mes MAC filter sur ma Freebox')
    print('9. Quitter')
    choice = input('> Que voulez vous faire ? ')

    print('')
    print('Ok faisons ça...')
    print('')
    if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        if choice == '1':
            maFreebox.getAllStaticIp()
        if choice == '2':
            maFreebox.pushConfigDHCP(input('Quel est le fichier à charger ?'))
        if choice == '3':
            maFreebox.getAllPortForwarding()
        if choice == '4':
            maFreebox.pushPortForwarding(input('Quel est le fichier à charger ?'))
        if choice == '5':
            maFreebox.getAllWifiGuest()
        if choice == '6':
            maFreebox.pushWifiGuest(input('Quel est le fichier à charger ?'))
        if choice == '7':
            maFreebox.getAllMacFilter()
        if choice == '8':
            maFreebox.pushMacFilter(input('Quel est le fichier à charger ?'))
        if choice == '9':
            quit()

        menu()
    else:
        menu()
##############################################

print('#########################################################')
print('#                    Save My Freebox                    #')
print('#########################################################')
print('')
print('')

menu()

#test add a static IP
#res = addStaticIp(s, "96:C6:30:58:B2:80", "192.168.1.3", "RedMiNote9Pro-Lu")