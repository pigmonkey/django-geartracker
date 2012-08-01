def metric(grams):
    """ Converts grams to kilograms if grams are greater than 1,000. """
    grams = int(grams)
    if grams >= 1000:
        kilograms = 0
        kilograms = grams / 1000.0
        # If there is no remainder, convert the float to an integer
        # so that the '.0' is removed.
        if not (grams % 1000):
            kilograms = int(kilograms)
        return u'%s %s' % (str(kilograms), 'kg')
    else:
        return u'%s %s' % (str(grams), 'g')


def imperial(grams):
    """
    Converts grams to ounces.

    If ounces are greater than 24, they are converted to pounds.
    """
    grams = int(grams)
    ounces = grams * 0.0352739619

    if ounces > 24:
        pounds = ounces / 16
        return u'%s %s' % (str(round(pounds, 2)), 'lb')

    return u'%s %s' % (str(round(ounces, 2)), 'oz')
