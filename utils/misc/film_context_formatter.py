

async def context_formatter(context: str):
    context = context.split()
    ganer = ''
    name = ''
    for item in context:
        if item.startswith('#'):
            ganer += item + ' '
        else:
            name += item + ' '

    return ganer.strip(), name.strip()
