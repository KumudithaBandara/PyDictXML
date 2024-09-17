Summary
=======

PyDictXML is a high-performance Python library designed to seamlessly replace dicttoxml, offering users an improved experience in XML string generation. With PyDictXML, users can effortlessly transition from dicttoxml without any code-level changes, benefiting from enhanced performance and efficiency.

Details
=======

Supports item (`int`, `float`, `long`, `decimal.Decimal`, `bool`, `str`, `unicode`, `datetime`, `none` and other number-like objects) and collection (`list`, `set`, `tuple` and `dict`, as well as iterable and dict-like objects) data types, with arbitrary nesting for the collections. Items with a `datetime` type are converted to ISO format strings. Items with a `None` type become empty XML elements.

The root object passed into the `dicttoxml` method can be any of the supported data types.

To satisfy XML syntax, the method prepends an `<?xml version="1.0" encoding="UTF-8" ?>` element and wraps the output in a `<root> ... </root>` element. However, this can be disabled to create XML snippets. Alternately, a custom root element can be specified by passing in the optional `custom_root=foobar` argument.

When dealing with lists of items, if each item itself is a collection data type such as `lists` or `dict`. Additionally, you have the option to assign a custom name to these elements using the item_func parameter if desired.

Each element can optionally include a `type` attribute indicating the data type. By default, this attribute is included, but you can exclude it by passing an optional `attr_type=False` argument when invoking the `dicttoxml` method.

Note: `datetime` data types are converted into ISO format strings, and `datetime` data types get a `str` attribute.

    Python -> XML
    integer   int
    long      long
    float     float
    Decimal   number
    string    str
    unicode   str
    datetime  str
    None      null
    boolean   bool
    list      list
    set       list
    tuple     list
    dict      dict

Elements with an unsupported data type raise a TypeError exception.

If an element name is invalid XML, it is rendered with the name "key" and the invalid name is included as a `name` attribute. E.g. `{ "^.{0,256}$": "foo" }` would be rendered `<key name="^.{0,256}$">foo</key>`. An exception is element names with spaces, which are converted to underscores.

**This module should work in Python 3.6+.**

Installation
============

The dicttoxml module is [published on the Python Package Index](https://pypi.python.org/pypi/dicttoxml), so you can install it using `pip`.

    pip install PyDictXML

Alternately, you can download the tarballed installer - `dicttoxml-[VERSION].tar.gz` - for this package from the [dist](https://github.com/quandyfactory/dicttoxml/tree/master/dist) directory on github and uncompress it. Then, from a terminal or command window, navigate into the unzipped folder and type the command:

    python setup.py install

That should be all you need to do.

Basic Usage
===========

Once installed, import the library into your script and convert a dict into xml by running the `dicttoxml` function:

    >>> import dicttoxml
    >>> xml = dicttoxml.dicttoxml(some_dict)

Alternately, you can import the `dicttoxml()` function from the library.

    >>> from dicttoxml import dicttoxml
    >>> xml = dicttoxml(some_dict)

That's it!

JSON to XML
===========

Let's say you want to fetch a JSON object from a URL and convert it into XML. Here's how you can do that:

    >>> import json
    >>> import urllib
    >>> import dicttoxml
    >>> page = urllib.urlopen('http://quandyfactory.com/api/example')
    >>> content = page.read()
    >>> obj = json.loads(content)
    >>> print(obj)
    {u'mylist': [u'foo', u'bar', u'baz'], u'mydict': {u'foo': u'bar', u'baz': 1}, u'ok': True}
    >>> xml = dicttoxml.dicttoxml(obj)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><mylist><item type="str">foo</item><item type="str">bar</item><item type="str">baz</item></mylist><mydict><foo type="str">bar</foo><baz type="int">1</baz></mydict><ok type="bool">true</ok></root>

It's that simple.

XML Snippet
===========

Instead of creating a full XML document, you can create an XML snippet for inclusion into another XML document.

Continuing with the example from above:

    >>> xml_snippet = dicttoxml.dicttoxml(obj, root=False)
    >>> print(xml_snippet)
    <mylist><item type="str">foo</item><item type="str">bar</item><item type="str">baz</item></mylist><mydict><foo type="str">bar</foo><baz type="int">1</baz></mydict><ok type="bool">true</ok>

With the optional `root` argument set to `False`, the method converts the dict into XML without including an `<?xml>` prolog or a `<root>` element to enclose all the other elements.

Custom Root
===========

By default, dicttoxml wraps all the elements in a `<root> ... </root>` element. Starting in version 1.5, you can change the name of the root element to something else by passing an optional `custom_root=some_custom_root` argument to the `dicttoxml` method.

Using our example:

    >>> xml = dicttoxml.dicttoxml(obj, custom_root='some_custom_root')
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><some_custom_root><mydict><foo>bar</foo><baz>1</baz></mydict><mylist><item>foo</item><item>bar</item><item>baz</item></mylist><ok>true</ok></some_custom_root>

As you can see, the name of the root element has changed to `some_custom_root`.

Omit XML Declaration
====================

Perhaps you want your outputted XML to have a `root` but no XML declaration. Starting with version 1.7.15, can call `dicttoxml` with the optional `xml_declaration` argument set to `False`:

    >>> xml = dicttoxml.dicttoxml(xml_declaration=False)
    >>> print(xml)
    <root><ok type="bool">true</ok><mylist type="list"><item type="str">foo</item><item type="str">bar</item><item type="str">baz</item></mylist><mydict type="dict"><foo type="str">bar</foo><baz type="int">1</baz></mydict></root>

As you can see, the XML declaration has been omitted.

Disable Type Attributes
=======================

By default, dicttoxml includes a type attribute for each element. Starting in version 1.4, you can turn this off by passing an optional `attr_type=False` argument to the `dicttoxml` method.

Using our example:

    >>> xml = dicttoxml.dicttoxml(obj, attr_type=False)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><mydict><foo>bar</foo><baz>1</baz></mydict><mylist><item>foo</item><item>bar</item><item>baz</item></mylist><ok>true</ok></root>

As you can see, the only difference is that the type attributes are now absent.

Change or Suppress XML Encoding Attribute
=========================================

By default, dicttoxml renders the XML element with an `encoding="UTF-8"` attribute. Starting in version 1.7.6, you can change the encoding by using the optional `encoding` argument to the `dicttoxml` method. For example, to render an XML file with encoding "ISO-8859-1", you would call:

    >>> xml = dicttoxml.dicttoxml(obj, encoding="ISO-8859-1")

Or if you prefer, you can suppress the encoding attribute altogether by setting the optional `include_encoding` argument to `False`:

    >>> xml = dicttoxml.dicttoxml(obj, include_encoding=False)

Again, by default, the `include_encoding` argument is set to `True` and the `encoding` argument is set to `UTF-8`.

Unique ID Attributes
====================

Starting in version 1.1, you can set an optional `ids` parameter so that dicttoxml gives each element a unique `id` attribute.

With the `ids` flag on, the function generates a unique randomly-generated ID for each element based on the parent element in the form `parent_unique`. For list items, the id is in the form `parent_unique_index`.

Continuing with our example:

    >>> xml_with_ids = dicttoxml.dicttoxml(obj, ids=True)
    >>> print(parseString(xml_with_ids).toprettyxml())
    <?xml version="1.0" ?>
    <root>
            <mylist id="root_160980" type="list">
                    <item id="mylist_609405_1" type="str">foo</item>
                    <item id="mylist_609405_2" type="str">bar</item>
                    <item id="mylist_609405_3" type="str">baz</item>
            </mylist>
            <mydict id="root_140407" type="dict">
                    <foo id="mydict_260437" type="str">bar</foo>
                    <baz id="mydict_111194" type="int">1</baz>
            </mydict>
            <ok id="root_612831" type="bool">true</ok>
    </root>

Note that the default XML output remains the same as previous, so as not to break compatibility for existing uses.

Dict-Like and Iterable Objects
==============================

Starting in version 1.3, dicttoxml accepts dict-like objects that are derived from the `dict` base class and treats them like dicts. For example:

    >>> import collections
    >>> dictlike = collections.OrderedDict({'foo': 1, 'bar': 2, 'baz': 3})
    >>> xml = dicttoxml.dicttoxml(dictlike)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><baz type="int">3</baz><foo type="int">1</foo><bar type="int">2</bar></root>

Also starting in version 1.3, dicttoxml accepts iterable objects and treats them like lists. For example:

    >>> myiter = range(1,11)
    >>> xml = dicttoxml.dicttoxml(myiter)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><item type="int">1</item><item type="int">2</item><item type="int">3</item><item type="int">4</item><item type="int">5</item><item type="int">6</item><item type="int">7</item><item type="int">8</item><item type="int">9</item><item type="int">10</item></root>

As always, this remains compatible with arbitrary nesting of objects and types.

Define Custom Item Names
========================

Starting in version 1.7, if you don't want item elements in a list to be called 'item', you can specify the element name using a function that takes the parent element name (i.e. the list name) as an argument.

    >>> import dicttoxml
    >>> obj = {u'mylist': [u'foo', u'bar', u'baz'], u'mydict': {u'foo': u'bar', u'baz': 1}, u'ok': True}
    >>> my_item_func = lambda x: 'list_item'
    >>> xml = dicttoxml.dicttoxml(obj, item_func=my_item_func)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><mydict type="dict"><foo type="str">bar</foo><baz type="int">1</baz></mydict><mylist type="list"><list_item type="str">foo</list_item><list_item type="str">bar</list_item><list_item type="str">baz</list_item></mylist><ok type="bool">True</ok></root>

The benefit of taking the parent element name as an argument is that you can write the function to do something with it. Let's say you have an object with some lists of specific items:

    >>> obj = {'shrubs': ['abelia', 'aralia', 'aucuba', 'azalea', 'bamboo', 'barberry', 'bluebeard', 'boxwood', 'camellia', 'dogwood', 'elderberry', 'enkianthus', 'firethorn', 'fuchsia', 'hazel', 'heath', 'heather', 'holly', 'honeysuckle', 'hydrangea', 'laurel', 'lilac', 'mock orange', 'rhododendron', 'rose', 'rose of sharon', 'rosemary', 'smokebush', 'spirea', 'sweetbox', 'viburnum', 'weigela', 'yucca'], 'trees': ['ash', 'aspen', 'birch', 'butternut', 'cedar', 'cottonwood', 'elm', 'fir', 'hawthorn', 'larch', 'locust', 'maple', 'oak', 'pine', 'spruce', 'sycamore', 'willow']}

You can define each item name to be the singular of its parent name by returning all but the last character.

    >>> my_item_func = lambda x: x[:-1]
    >>> xml = dicttoxml.dicttoxml(obj, item_func=my_item_func)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><shrubs type="list"><shrub type="str">abelia</shrub><shrub type="str">aralia</shrub><shrub type="str">aucuba</shrub><shrub type="str">azalea</shrub><shrub type="str">bamboo</shrub><shrub type="str">barberry</shrub><shrub type="str">bluebeard</shrub><shrub type="str">boxwood</shrub><shrub type="str">camellia</shrub><shrub type="str">dogwood</shrub><shrub type="str">elderberry</shrub><shrub type="str">enkianthus</shrub><shrub type="str">firethorn</shrub><shrub type="str">fuchsia</shrub><shrub type="str">hazel</shrub><shrub type="str">heath</shrub><shrub type="str">heather</shrub><shrub type="str">holly</shrub><shrub type="str">honeysuckle</shrub><shrub type="str">hydrangea</shrub><shrub type="str">laurel</shrub><shrub type="str">lilac</shrub><shrub type="str">mock orange</shrub><shrub type="str">rhododendron</shrub><shrub type="str">rose</shrub><shrub type="str">rose of sharon</shrub><shrub type="str">rosemary</shrub><shrub type="str">smokebush</shrub><shrub type="str">spirea</shrub><shrub type="str">sweetbox</shrub><shrub type="str">viburnum</shrub><shrub type="str">weigela</shrub><shrub type="str">yucca</shrub></shrubs><trees type="list"><tree type="str">ash</tree><tree type="str">aspen</tree><tree type="str">birch</tree><tree type="str">butternut</tree><tree type="str">cedar</tree><tree type="str">cottonwood</tree><tree type="str">elm</tree><tree type="str">fir</tree><tree type="str">hawthorn</tree><tree type="str">larch</tree><tree type="str">locust</tree><tree type="str">maple</tree><tree type="str">oak</tree><tree type="str">pine</tree><tree type="str">spruce</tree><tree type="str">sycamore</tree><tree type="str">willow</tree></trees></root>

Of course, this can be combined with other optional arguments, like disabling type attributes or custom root element names.

CDATA
=====

Starting in version 1.7.1, you can wrap values in CDATA by setting the optional `cdata` argument to `True`.

    >>> import dicttoxml
    >>> obj = {u'mylist': [u'foo', u'bar', u'baz'], u'mydict': {u'foo': u'bar', u'baz': 1}, u'ok': True}
    >>> xml = dicttoxml.dicttoxml(obj, cdata=True)
    >>> print(xml)
    <?xml version="1.0" encoding="UTF-8" ?><root><mydict type="dict"><foo type="str"><![CDATA[bar]]></foo><baz type="int"><![CDATA[1]]></baz></mydict><mylist type="list"><item type="str"><![CDATA[foo]]></item><item type="str"><![CDATA[bar]]></item><item type="str"><![CDATA[baz]]></item></mylist><ok type="bool"><![CDATA[True]]></ok></root>

If you do not set `cdata` to `True`, the default value is `False` and values are not wrapped.

Return a String
===============

By default, dicttoxml outputs the generated XML as a `bytes` object:

    >>> xml = dicttoxml.dicttoxml(obj)
    >>> type(xml).__name__
    'bytes'

Starting in version 1.7.14, when you call the dicttoxml function, you can set an optional `return_bytes` argument to `False` to return a `str` object instead:

    >>> xml = dicttoxml.dicttoxml(obj, return_bytes=False)
    >>> type(xml).__name__
    'str'

But by default, `return_bytes` is set to `True`.

Pretty-Printing
===============

As they say, Python comes with batteries included. You can easily syntax-check and pretty-print your XML using Python's `xml.dom.minidom` module.

Again, continuing with our example:

    >>> from xml.dom.minidom import parseString
    >>> dom = parseString(xml)
    >>> print(dom.toprettyxml())
    <?xml version="1.0" ?>
    <root>
        <mylist type="list">
            <item type="str">foo</item>
            <item type="str">bar</item>
            <item type="str">baz</item>
        </mylist>
        <mydict type="dict">
            <foo type="str">bar</foo>
            <baz type="int">1</baz>
        </mydict>
        <ok type="bool">true</ok>
    </root>

This makes the XML easier to read. If it is not well-formed, the xml parser will raise an exception.

Debugging
=========

You can enable debugging informationby calling the `set_debug()` method:

    >>> import dicttoxml
    >>> dicttoxml.set_debug(debug=True)
    Debug mode is on. Events are logged at: dicttoxml.log
    >>> xml = dicttoxml.dicttoxml(some_dict)

By default, debugging information is logged to `dicttoxml.log`, but you can change this:

    >>> dicttoxml.set_debug(debug=True, filename='/path/to/some_other_filename.log')
    Debug mode is on. Events are logged at: some_other_filename.log

To turn debug mode off, just call `set_debug` with an argument of `False`:

    >>> dicttoxml.set_debug(debug=False)

If you encounter any errors in the code, please file an issue on github: [https://github.com/KumudithaBandara/PyDictXML/issues](https://github.com/KumudithaBandara/PyDictXML/issues).

Author
======

* Author: Kumuditha Bandara
* Repository: [https://github.com/KumudithaBandara/PyDictXML](https://github.com/KumudithaBandara/PyDictXML)

Version
=======

* Version: 1.0.0
* Release Date: 2024-02-04

Revision History
================

Version 1.0.1
--------------

* Release Date: 2024-09-17
* Changes:
    * Now package import similar to dicttoxml

Version 1.0.0
--------------

* Release Date: 2024-02-04
* Changes:
    * Initial release



Copyright and Licence
=====================

Copyright 2024 by Kumuditha Bandara.

Released under the GNU General Public Licence, Version 2:  
<http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
