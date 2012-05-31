
print "<!DOCTYPE html><html><body>"

option = request.POST.get('selection')
if not option:
    print "Nothing selected."
else:
    print "You selected %s." % option[0]

print "</body></html>"