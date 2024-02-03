import timeit
import xml.etree.ElementTree as ET
from lxml import etree
from DictToXML import dicttoxml as DictToXML
import DictToXML2
import dicttoxml
from json2xml import json2xml

# Sample dictionary with various data types
sample_dict = {
    'person': {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York',
        'is_student': True,
        'grades': [90, 85, 88],
        'address': {
            'street': '123 Main St',
            'zip_code': 10001
        },
        'friends': [
            {'name': 'Alice', 'age': 28},
            {'name': 'Bob', 'age': 32}
        ],
        'notes': ('This is a long note.' * 1000 ) # Add a long string
    },
    'pi': 3.14159,
    'colors': ['red', 'green', 'blue'],
    'nested_lists': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    'empty_dict': {},
    'empty_list': []
}


# Define conversion functions
def DictToXML_convert():
    output = DictToXML(sample_dict)
    return output


def DictToXML2_convert():
    output = DictToXML2.dicttoxml(sample_dict)
    return output


def etree_convert():
    root = ET.Element("root")
    dict_to_etree(sample_dict, root)
    output = ET.tostring(root)
    return output


def lxml_convert():
    root = etree.Element("root")
    dict_to_etree(sample_dict, root)
    output = etree.tostring(root, pretty_print=True)
    return output


def dicttoxml_convert():
    output = dicttoxml.dicttoxml(sample_dict)
    return output


def json2xml_convert():
    xml_data = json2xml.Json2xml(sample_dict).to_xml()
    return xml_data


# Define a function to convert dict to xml using xml.etree.ElementTree
def dict_to_etree(d, parent):
    for key, value in d.items():
        if isinstance(value, dict):
            child = ET.Element(key) if isinstance(parent, ET.Element) else etree.Element(key)
            parent.append(child)
            dict_to_etree(value, child)
        elif isinstance(value, list):
            for item in value:
                child = ET.Element(key) if isinstance(parent, ET.Element) else etree.Element(key)
                child.text = str(item)
                parent.append(child)
        else:
            child = ET.Element(key) if isinstance(parent, ET.Element) else etree.Element(key)
            child.text = str(value)
            parent.append(child)


# Perform benchmarking for different numbers of iterations
num_iterations_list = [1, 10, 100, 500, 1000, 2000, 5000]

for num_iterations in num_iterations_list:
    print(f"\n\nBenchmarking for {num_iterations} iterations:")
    results = {}

    results['DictToXML'] = timeit.timeit(DictToXML_convert, number=num_iterations)
    # results['DictToXML2'] = timeit.timeit(DictToXML2_convert, number=num_iterations)
    # results['xml.etree.ElementTree'] = timeit.timeit(etree_convert, number=num_iterations)
    # results['lxml'] = timeit.timeit(lxml_convert, number=num_iterations)
    results['dicttoxml'] = timeit.timeit(dicttoxml_convert, number=num_iterations)
    # results['jsontoxml'] = timeit.timeit(json2xml_convert, number=num_iterations)

    # Sort results by execution time
    sorted_results = sorted(results.items(), key=lambda x: x[1])

    # Print results
    print("\nPerformance Comparison (sorted by fastest):")
    for method, time_taken in sorted_results:
        print(f"{method}: {time_taken} seconds")

    # Calculate percentages relative to the fastest method
    fastest_time = sorted_results[0][1]
    percentages = {method: (time_taken / fastest_time) * 100 for method, time_taken in sorted_results}

    # Print results with correct comparisons
    print("\nPerformance Comparison (sorted by fastest):")
    for i in range(len(sorted_results)):
        for j in range(i + 1, len(sorted_results)):
            method1, time_taken1 = sorted_results[i]
            method2, time_taken2 = sorted_results[j]

            if time_taken1 < time_taken2:
                percentage_difference = (time_taken2 - time_taken1) / time_taken2 * 100
                print(
                    f"{method1} is {percentage_difference:.2f}% ({time_taken2 / time_taken1:.2f} times) faster than {method2}")
            elif time_taken1 > time_taken2:
                percentage_difference = (time_taken1 - time_taken2) / time_taken1 * 100
                print(
                    f"{method2} is {percentage_difference:.2f}% ({time_taken1 / time_taken2:.2f} times) faster than {method1}")
            else:
                print(f"{method1} and {method2} have equal performance")



