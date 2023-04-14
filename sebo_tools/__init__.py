import click


def validate_resolution(ctx, param, value):
    """Validate a resolution in the format WIDTHxHEIGHT as a Click option.

    This function exists because 'Wand.Image.transform' always marks images as dirty
    when the 'resize' keyword argument is passed. And parsing the width and height of
    a resolution is a prerequisite to avoiding making a call to 'transform'.
    """

    if isinstance(value, tuple):
        return value

    try:
        max_width, _, max_height = value.partition("x")
        return int(max_width), int(max_height)
    except ValueError:
        raise click.BadParameter("format must be 'WIDTHxHEIGHT'")
