# Lament

__"An easy way to handle application configuration (and open a schism to a dimention of endless pain and suffering)."__

## Example

Here I will go through a number of examples and explain the finer details of how to write a configuration parser using Lament.

First things first, here is the simplest example imaginable, a parser with a single option that simply overwrites the privious value but does no type checking:

```
class Example(LamentConfig):
    # 'myConfigOption': 'abc'
    #     -> lamentconfig.myConfigOption = 'abc'
    @config('myConfigOption', str)
    def myConfigOption(self, old, new):
        return new
```

Each parser inherits `LamentConfig` and each option has a decorated handler function. In this case the decorator is `@config` and takes two params, the name of the option and it's default type.

The handler function itself also takes two params, `old` and `new`. `old` is the current value of that option (If the option's value is never set it is infered to be the default return value of the type, so in this case `str()`). `new` is the value that was read from the config file. Because Lament stores config in JSON format, most of the time these values will be strings or numbers, but they can also be lists or dicts. If you want Lament to hold these in the form of some custom object, this handler is your chance to convert it. Anything you return will be set as the new value.

```
    # 'myConfigOption': 5
    #     -> lamentconfig.myConfigOption = CustomType(5)
    @config('myConfigOption', CustomType)
    def myConfigOption(self, old, new):
        if isinstance(new, int):
            return CustomType(new)
        else:
            logging.warn('can't use type %s as a value for myConfigOption' % type(new))
            return old
```

In the above example, the input is checked to make sure it's an `int`, then it's used to instansiate a new `CustomType` object. If someone accidentally passes in the wrong type, it warns them and sticks with the old config value.

```
    # 'myConfigOption': 'abc'
    #     -> lamentconfig.myConfigOption.add('abc')
    # 'myConfigOption': 'abc!'
    #     -> lamentconfig.myConfigOption.discard('abc')
    @config('myConfigOption', set)
    def myConfigOption(self, old, new):
        if isinstance(new, str) 
            if new[-1] == '!':
                old.discard(new)
                return old
            else:
                old.add(new)
                return old
        else:
            logging.warn('can't use type %s as a value for myConfigOption' % type(new))
            return old
```

This is a complex example where the config option stores a `set` of strings. If the `str` provided in the config ends with an '!', it's removed from the set, otherwise it's added.

### Example using regexs

You can also create a config options that behave like dictionaries, holding multiple key/value pairs. Best of all, you can control which of the keys are valid with regular expressions. This is done with the `@regex_config` decorator:

```
    # 'host www.mydomain.ie': 'localhost:80'
    #     -> lamentconfig.host['www.mydomain.ie'] = ('localhost', 80)
    @regex_config('hosts', '.*', tuple)
    def hosts(self, old, new):
        host, port = new.split(':')[:1]
        return (host, int(port))
```

The `@regex_config` decorator takes 3 params, the option name, a regular expression used to filter keys and the default type. Apart from that the method acts just like the other handlers.

### Exporting custom data

You can also explicitly define handlers to be used for any config option during export. This is especially handy if you've stored the data with a custom type.

```
    @export('numbers')
    def export_numbers(self, obj):
        return [z for z in obj if isinstance(z, int)]
```

With these handlers you just receive the current value of that config option, in this case it's named `obj`, which gets filtered so as to only return values of type int. Lament takes the return value and dumps it to the new (JSON) config file.

## The Lament Configuration

This project's name was inspired by the puzzle box in the [Hellraiser movies](http://en.wikipedia.org/wiki/Lemarchand%27s_box).

## Licence

`lament` is released under the [MIT License](http://opensource.org/licenses/MIT).
