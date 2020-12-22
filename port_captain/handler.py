"""
AWS Lambda event handler


"""


def port_captain_lambda(event, context):
    """ Redirect data for `thing/*` AWS IoT core topics
    to desired processing chain
    """

