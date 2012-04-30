"""dom_helpers.py:  Helper functions for the XML Document Object Model
    $Revision: 1.12 $  $Date: 2003/03/16 01:04:40 $

  Exports:
    textContent ( node ):
      [ if node has any #text content nodes ->
          return the content of all such nodes as a string
        else -> return None ]
    getChildContent ( node, childName ):
      [ if (node is a minidom Element object)
        and (childName is a string) ->
          if (node has a child whose name matches childName)
          and (that child has at least one #text child) ->
            return the content all those #text children as a string
          else -> return None ]
    getChildIntContent ( node, childName ):
      [ if (node is a minidom Element object)
        and (childName is a string) ->
          if (node has a child whose name matches childName and
          which has text content that is a valid integer ->
            return that content as an integer
          else -> raise ValueError ]
    getChildFloatContent ( node, childName ):
      [ if (node is a minidom Element object)
        and (childName is a string) ->
          if (node has a child whose name matches childName and
          which has text content that is a valid float ->
            return that content as a float
          else -> raise ValueError ]
    getAttr ( node, attrName, default=None ):
      [ if (node is a minidom Element object)
        and (attrName is a string) ->
          if node has an attribute named (attrName) ->
            return that attribute as a string
          else -> return default ]
    getChildList ( node, childName, f ):
      [ if (node is a minidom Element object)
        and (childName is a string)
        and (f is a node-to-object function) ->
          return a list of objects [f(e0), f(e1), ...] where
          [e0, e1, ...] are the descendants of node whose name matches
          childName ]
    getChildIfAny ( node, childName ):
      [ if (node is a minidom Element object)
        and (childName is a string) ->
            return the first such child as an Element object
        else -> return None ]
"""

#================================================================
# Verification functions
#----------------------------------------------------------------
# node-to-object ==
#   an object constructor f with calling sequence
#     f(elt)
#   and intended function
#     [ if elt is a minidom Element object ->
#         return a new object representing elt ]
#----------------------------------------------------------------



# - - -   t e x t C o n t e n t   - - -

def textContent ( node ):
    "Return the text content of a node (if any, else return None)."

    #-- 1 --
    result  =  []

    #-- 2 --
    # [ result  :=  result + (strings from #text children of node if any) ]
    for  child in node.childNodes:
        #-- 2 body --
        # [ if  child is a #text node ->
        #     result  :=  result + (that child's content as a string)
        #   else -> I ]
        if  child.nodeName == "#text":
            result.append ( str ( child.data ) )

    #-- 3 --
    # [ if result is empty ->
    #     return None
    #   else ->
    #     return elements of result, concatenated ]
    if  len ( result ) == 0:
        return None
    else:
        return "".join(result)


# - - -   g e t C h i l d C o n t e n t   - - -

def getChildContent ( node, childName ):
    "Extracts the content of #text children of an Element node."

    #-- 1 --
    # [ if node has a child whose name matches childName ->
    #     child  :=  an Element node representing that child
    #   else -> return None ]
    childList  =  node.getElementsByTagName ( childName )

    if  len ( childList ) < 1:
        return None
    else:
        child  =  childList[0]

    #-- 2 --
    # [ if child has a child of type #text ->
    #     textNode  :=  a Text object representing the last such child
    #   else -> return None ]
    return textContent ( child )


# - - -   g e t C h i l d I n t C o n t e n t   - - -

def getChildIntContent ( node, childName ):
    "Like getContent(), but requires that the text be a valid int."

    #-- 1 -
    # [ if (node has a child whose name matches childName)
    #   and (that child has at least one #text child) ->
    #     raw  :=  the content from the last #text child as a string
    #   else -> raise ValueError ]
    raw  =  getContent ( node, childName )
    if  raw is None:
        raise ValueError, ( "Node <%s>, missing <%s> or bad content" %
            ( node.nodeName, childName ) )
    #-- 2 --
    # [ if raw is a valid integer ->
    #     return raw as a integer
    #   else -> raise ValueError ]
    return int ( raw )


# - - -   g e t C h i l d F l o a t C o n t e n t   - - -

def getChildFloatContent ( node, childName ):
    "Like getContent(), but requires that the text be a valid float."

    #-- 1 -
    # [ if (node has a child whose name matches childName)
    #   and (that child has at least one #text child) ->
    #     raw  :=  the content from the last #text child as a string
    #   else -> raise ValueError ]
    raw  =  getContent ( node, childName )
    if  raw is None:
        raise ValueError, ( "Node <%s> has no <%s> children" %
            ( node.nodeName, childName ) )

    #-- 2 --
    # [ if raw is a valid float ->
    #     return raw as a float
    #   else -> raise ValueError ]
    return float ( raw )


# - - -   g e t A t t r   - - -

def getAttr ( node, attrName, default=None ):
    "Extract and return an attribute, or default if it hasn't one."

    #-- 1 --
    # [ if node has an attribute named attrName ->
    #     result  :=  that attribute's value as a string
    #   else ->
    #     result  :=  "" ]
    result  =  node.getAttribute ( attrName )

    #-- 2 --
    # [ if result is "" ->
    #     return default
    #   else ->
    #     return result, converted to type string (from Unicode) ]
    if  len ( result ) == 0:
        return default
    else:
        return str(result)


# - - -   g e t C h i l d L i s t   - - -

def getChildList ( node, childName, f ):
    """Turn certain descendant nodes into a list of objects.
    """

    #-- 1 --
    # [ eltList  :=  a list of the (childName) descendants of node
    #   result   :=  a new, empty list ]
    eltList  =  node.getElementsByTagName ( childName )
    result  =  []

    #-- 2 --
    # [ result  :=  result with objects appended
    #       made by applying f to the elements of eltList ]
    for  elt in eltList:
        result.append ( f ( elt ) )

    #-- 3 --
    return result


# - - -   g e t C h i l d I f A n y   - - -

def getChildIfAny ( node, childName ):
    "Return the first or only named descendant node, or None."

    #-- 1 --
    # [ childList  :=  a list of (childName) descendants of node ]
    childList  =  node.getElementsByTagName ( childName )

    #-- 2 --
    if  len ( childList ) < 1:
        return None
    else:
        return childList[0]
