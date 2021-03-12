import os
import click

from selfInstall import createApp, db
from selfInstall.models.users import User
app = createApp(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User}

@app.cli.command("add-user", short_help="Add a new user")
@click.argument("email")
@click.option(
    "--admin", is_flag=True, default=False, help="Grant administrator role"
)
def addUser(email, admin,):
    """Add a new user to the database with email address = EMAIL."""
    if User.findByEmail(email):
        error = f"Error: {email} is already registered"
        click.secho(f"{error}\n", fg="red", bold=True)
        return 1
    newUser = User(email=email, admin=admin)
    db.session.add(newUser)
    db.session.commit()
    userType = "admin user" if admin else "user"
    newUserToken=newUser.encodeAccessToken()
    message = f"Successfully added new {userType}:\n {newUser} \n JWT: {newUserToken}"
    click.secho(message, fg="blue", bold=True)
    return 0
