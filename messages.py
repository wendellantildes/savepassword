import gettext 
import locale
import platform


so = platform.system()
language = "pt_br"
_ = gettext.gettext
if(language == "pt_br"):
    PT_BR = gettext.translation('app', './locale', languages=['pt_BR'])
    PT_BR.install()
    if(so == "Windows"):
        PT_BR.set_output_charset('cp850')
    _ = PT_BR.gettext
else:
    locale.setlocale(locale.LC_ALL, '')
    if(so == "Windows"):
        gettext.bindtextdomain('app', ['./locale','cp850'])
    else:
        gettext.bindtextdomain('app', './locale')
    gettext.textdomain('app')

authentication_password_error  = _("Wrong password")
authentication_email_error     = _("Email not exist")
authentication_authenticated   = _("Authenticated")
authentication_welcome         = _("###Welcome {name} =)")
authentication_expired_session = _("***Expired session. Some features may require your login")
authentication_session_begin   = _("Session started at %s")
authentication_session_end     = _("Session will expire at %s")
authentication_session_error   = _("Start of session failed")

prompt_command_error              = _("Command not exists. --Type 'help' to see the commands")
prompt_command_name               = _("Type your name: ")
prompt_command_name_error         = _("Typed name is empty")
prompt_command_email              = _("Type your email(It will be your login): ")
prompt_command_email_error        = _("Invalid email")
prompt_command_email_duplicated   = _("Email already exists")
prompt_command_password           = _("Type your password (Don't forget it because you won't be able to retrieve it): ")
prompt_command_password_error_empty = _("Password empty")
prompt_command_password_again     = _("Type your password again (Don't forget it because you won't be able to retrieve it): ")
prompt_command_password_error     = _("Password doesn't match")
prompt_command_operation_aborted  = _("**Operation aborted**")
prompt_command_user_added         = _("User added")

prompt_command_login_email        = _("Type your email")
prompt_command_login_password     = _("Type your password")
prompt_command_login_required     = _("You must be logged to perform this operation")

prompt_command_logout             = _("Logout done with success")

prompt_command_account_name           = _("Type the account name: ")
prompt_command_account_name_duplicated = _("Name already exists")
prompt_command_account_title          = _("Type the account title: ")
prompt_command_account_title_error    = _("Typed title is empty")
prompt_command_account_login          = _("Type the account login: ")
prompt_command_account_login_error    = _("Typed login is empty")
prompt_command_account_password       = _("Type the account password: ")
prompt_command_account_password_error = _("Typed password is empty")
prompt_command_account_site           = _("Type the account site (optional): ")
prompt_command_account_description    = _("Type the account description (optional): ")
prompt_command_account_added          = _("Account added")

prompt_command_more                   = _("more...")


prompt_command_list_accounts_id		 = _("id: ")
prompt_command_list_accounts_name		 = _("Name: ")
prompt_command_list_accounts_title		 = _("Title: ")
prompt_command_list_accounts_login		 = _("Login: ")
prompt_command_list_accounts_password    = _("Password: ")
prompt_command_list_accounts_site		 = _("Site: ")
prompt_command_list_accounts_description = _("Description: ")
prompt_command_list_accounts_no_account  = _("You have no account")

prompt_command_find_accounts_search = _("Search for: ")

prompt_command_delete_account_name    = _("Type the account name you want to delete: ")
prompt_command_delete_account_view    = _("***THIS ACCOUNT WILL BE DELETED***")
prompt_command_delete_account_confirm = _("Are you sure you want to delete this account? (type 'y' for yes and 'n' for no): ") 
prompt_command_delete_account_not_found = _("No account was found")
prompt_command_delete_account_deleted   = _("Account deleted with success")
prompt_command_delete_account_not_deleted = _("Account not deleted")

prompt_command_update_account             = _("Type the account name you want to update: ")
prompt_command_update_account_view        = _("THIS ACCOUNT WILL BE UPDATED")
prompt_command_update_account_confirm     = _("Are you sure you want to update this account? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_not_found   = _("No account was found")
prompt_command_update_account_updated     =_("Account updated with success")
prompt_command_update_account_not_updated = _("Account not updated")
prompt_command_update_account_name        = _("Update name? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_title       = _("Update title? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_login       = _("Update login? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_password    = _("Update password? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_site        = _("Update site? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_description = _("Update description? (type 'y' for yes and 'n' for no): ")
prompt_command_update_account_original_text = _("***Original text>>> ")
prompt_command_update_account_new_text      = _("New text>>>")

prompt_command_update_user_name_updated      = _("Name updated with success")
prompt_command_update_user_type_password       = _("Type the new password: ")
prompt_command_update_user_type_password_again = _("Type the new password again: ")
prompt_command_update_user_password_updated  = _("Password updated with success")
prompt_command_update_user_type_email       = _("Type the new email: ")
prompt_command_update_user_email_updated     = _("Email updated with success")

prompt_command_help_cancel = _("**Type 'CTRL+c' to cancel the current operation")
prompt_command_help_exit = _("--Type 'exit' to finish the program ")
prompt_command_help_add_user = _("--Type 'add user' to add a new user")
prompt_command_help_update_name = _("--Type 'update name' to update the user's name. **Login is required")
prompt_command_help_update_email = _("--Type 'update email' to update the user's email. **Login is required ")
prompt_command_help_update_password = _("--Type 'update password' to update user's password. **Login is required ")
prompt_command_help_login = _("--Type 'login' to login")
prompt_command_help_logout = _("--Type 'logout' to logout")
prompt_command_help_add_account = _("--Type 'add account' to add a new account. **Login is required")
prompt_command_help_update_account = _("--Type 'update account' to update an account. **Login is required")
prompt_command_help_delete_account = _("--Type 'delete account' to delete an account. **Login is required")
prompt_command_help_list_accounts = _("--Type 'list accounts' to list accounts. **Login is required")
prompt_command_help_find_account = _("--Type 'find accounts' to search accounts. **Login is required")

head = _("Portable Save Passwords \n --Type 'help' to see the commands")
