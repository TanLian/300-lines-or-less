#coding: utf-8
import re

class TemplateFileNotExist(Exception):
    pass

class KeyNotFound(Exception):
    pass

class IfNotValid(Exception):
    pass

class ForNotValid(Exception):
    pass

class Engine(object):
    def _do_dot(self, key_words, context, stay_func = False):
        if isinstance(context, dict):
            if key_words in context:
                return context[key_words]
            raise KeyNotFound('{key} is not found'.format(key=key_words))
        value = getattr(context, key_words)
        if callable(value) and not stay_func:
            value = value()
        return value
    def _do_dot_seq(self, key_words, context, stay_func = False):
        if not '.' in key_words:
            return self._do_dot(key_words, context, stay_func)
        k_lst = key_words.split('.')
        k_lst = [item.strip() for item in k_lst]
        result = context
        for item in k_lst:
            result = self._do_dot(item, result, stay_func)
        return repr(result)

class VarEngine(Engine):
    def _do_vertical_seq(self, key_words, context, top_context):
        if top_context is None:
            top_context = context
        k_lst = key_words.split('|')
        k_lst = [item.strip() for item in k_lst]
        result = self._do_dot_seq( k_lst[0], context)
        for filter in k_lst[1:]:
            try:
                func = self._do_dot_seq(filter, context, True)
            except KeyNotFound:
                func = self._do_dot_seq(filter, top_context, True)
            result = func(result)
        return result
    def __init__(self, k, context, top_context = None):
        self.result = self._do_vertical_seq(k, context, top_context) if '|' in k else self._do_dot_seq(k, context)

class IfEngine(Engine):
    def __init__(self, key_words, context):
        k_lst = key_words.split(' ')
        k_lst = [item.strip() for item in k_lst]
        if len(k_lst) % 2 == 1:
            raise IfNotValid
        for item in k_lst[2::2]:
            if item not in ['and', 'or']:
                raise IfNotValid
        cond_lst = k_lst[1:]
        index  = 0
        while index < len(cond_lst):
            cond_lst[index] = str(self._do_dot_seq(cond_lst[index], context))
            index += 2
        self.cond = eval(' '.join(cond_lst))

class IfBlock(object):
    def __init__(self, context, key_words, top_context=None):
        self.result = '' if not IfEngine(key_words[0][2:-2].strip(), context).cond else recursive_traverse(key_words[1:-1], context, top_context)

class ForBlock(Engine):
    def __init__(self, context, key_words):
        for_engine = key_words[0][2:-2].strip()
        for_engine_lst = for_engine.split(' ')
        for_engine_lst = [item.strip() for item in for_engine_lst]
        if len(for_engine_lst) != 4:
            raise ForNotValid
        if for_engine_lst[0] != 'for' or for_engine_lst[2] != 'in':
            raise ForNotValid
        iter_obj = self._do_dot_seq(for_engine_lst[3], context)
        self.result = ''
        for item in iter_obj:
            self.result += recursive_traverse(key_words[1:-1], {for_engine_lst[1]:item}, context)

def recursive_traverse(lst, context, top_context = None):
    if top_context is None:
        top_context = context
    stack, result = [], []
    is_if, is_for, times, match_times = False, False, 0, 0
    for item in lst:
        if item[:2] != '{{' and item[:2] != '{%':
            result.append(item) if not is_if and not is_for else stack.append(item)
        elif item[:2] == '{{':
            result.append(VarEngine(item[2:-2].strip(), context, top_context).result) if not is_if and not is_for else stack.append(item)
        elif item[:2] == '{%':
            expression = item[2:-2]
            expression_lst = expression.split(' ')
            expression_lst = [it for it in expression_lst if it]
            if expression_lst[0] == 'if':
                stack.append(item)
                if not is_for:
                    is_if = True
                    times += 1
            elif expression_lst[0] == 'for':
                stack.append(item)
                if not is_if:
                    is_for = True
                    times += 1
            if expression_lst[0] == 'endif':
                stack.append(item)
                if not is_for:
                    match_times += 1
                if match_times == times:
                    result.append(IfBlock(context, stack, top_context).result)
                    del stack[:]
                    is_if, is_for, times, match_times = False, False, 0, 0
            elif expression_lst[0] == 'endfor':
                stack.append(item)
                if not is_if:
                    match_times += 1

                if match_times == times:
                    result.append(ForBlock(context, stack).result)
                    del stack[:]
                    is_if, is_for, times, match_times = False, False, 0, 0

    return ''.join(result)

def fff(name):
    return name + ' RMB'

def main():
    template = '''
        <p>Welcome, {{ user_name }}!</p>
        <p>Products:</p>
        
        {% if is_show %}
            haha: {{ user_name | fff }}
        {% endif %}

        {% for product in product_list %}
            {% if product.show %}
                <li>{{ product.name }}:
                    {{ product.price | fff }}</li>
            {% endif %}
        {% endfor %}
        
        {% if is_show2 and is_show %}
            {% if is_show %}
                hehe: {{ user_name }}
            {% endif %}
        {% endif %}
    '''

    context = {
        'user_name':'tanlian',
        'is_show2':True,
        'is_show':True,
        'product_list': [
            {
                'show':True,
                'price':20,
                'name': 'Apple'
             },
            {
                'show': False,
                'price': 21,
                'name': 'Pear'
            },
            {
                'show': True,
                'price': 22,
                'name': 'Banana'
            },
        ],
        'fff': fff
    }
    tokens = re.split(r"(?s)({{.*?}}|{%.*?%})", template)
    print recursive_traverse(tokens, context)

main()