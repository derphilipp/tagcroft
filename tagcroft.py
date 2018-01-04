import click

@click.group()
def tagcroft():
    pass

@tagcroft.command()
def cmd1():
    '''Command on tagcroft'''
    click.echo('tagcroft cmd1')

@tagcroft.command()
def cmd2():
    '''Command on tagcroft'''
    click.echo('tagcroft cmd2')

if __name__ == '__main__':
    tagcroft()
