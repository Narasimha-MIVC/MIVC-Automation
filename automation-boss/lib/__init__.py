"""
    Common utilities to handle delayed responses from the DB
    Author: Prasanna
"""
import time


def wait_in_loop(func, *args, **kwargs):
    """
    This function waits in a loop till the element on the page is visible
    :param func: The Selenium function pointer
    :param args: Argument list to be passed to the Selenium function pointer
    :param kwargs: Keyword argument lists for local handling (e.g. "loop_count", "delay_in_sec", "return_value")
    :return: Return value of the selenium function
    """
    i_time = 0
    default_loop_count = kwargs.get('loop_count', 5)
    # default_loop_count = 25 if not default_loop_count else 5 * default_loop_count
    default_delay = kwargs.get('delay_in_sec', 5)
    for i in range(default_loop_count):
        time.sleep(i_time)     # first iteration without wait
        try:
            d = args[-1] if args else None   # if "func" requires key value arg lists. It should be the last in "args"
            if not kwargs.get('return_value', None):
                if d and isinstance(d, dict):
                    func(*args[:-1], **d)
                else:
                    func(*args)
                break
            else:
                if d and isinstance(d, dict):
                    v = func(*args[:-1], **d)
                else:
                    v = func(*args)
                return v
        except Exception as e:
            pass
        i_time = default_delay
    else:
        raise Exception("page load unsuccessful!")


def select_from_dropdown(func1, func2, *args, **kwargs):
    """
    This function selects an element from the drop down list.
    A lot of delay has been observed during this operation. This function will address the problem.
    :param func1: The function to get the list of the elements from the drop down list
    ("query_ele.get_text_list_from_dropdown")
    :param func2: The function that selects the element from the drop down list either on the basis of index or text
    ("action_ele.select_from_dropdown_using_text", "action_ele.select_from_dropdown_using_index")
    :param args: tuple of locator and value(index / text)
    :param kwargs: Keyword argument lists for local handling (e.g. "loop_count", "delay_in_sec")
    :return:
    """
    i_time = 0
    default_loop_count = kwargs.get('loop_count', 5)
    # default_loop_count = 25 if not default_loop_count else 5 * default_loop_count
    default_delay = kwargs.get('delay_in_sec', 5)
    if not args or len(args) < 2:
        raise Exception("Invalid Parameters ! Both Locator and Value required")
    for i in range(default_loop_count):
        time.sleep(i_time)     # first iteration without wait
        try:
            list_elements = func1(args[0])
            if isinstance(args[1], int) and args[1] < len(list_elements):
                func2(args[0], args[1])
                break
            elif args[1] in list_elements:
                func2(args[0], args[1])
                break
        except Exception as e:
            pass
        i_time = default_delay
    else:
        raise Exception("selecting element from the drop down failed!")