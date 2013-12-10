# Lament

An easy way to handle application configuration (and open a schism to a dimention of endless pain and suffering).

## Example

First things first, create a config parser by subclassing LamentConfig:

```
class Example(LamentConfig):
```

Then you can declare handlers for each config option. Any method in a LamentConfig subclass can be a config handler, you just need to attach the config decorator with the name of the config option and it's default type. For example you could have 'my_config_option' which acts just a list of values:

```
    @config('myConfigOption', list)
    def update_a(self, config, obj):
        return obj
```

In the above example, the handler receives two parameters: _config_ which is the current value of myConfigOption and _obj_ which is the value found for that option when you open a new config file. You're free to handle any changes to _config_ that you see fit and the value you return will be set as the new value for that config option. The above example has the effect of simply overriding the current list of values with those found in _obj_.

You can also explicitly define handlers to be used for any config option during export:

```
    @export('numbers')
    def export_numbers(self, obj):
        return [z for z in obj if isinstance(z, int)]
```

With these handlers you just receive the current value of that config option, is this case it's named _obj_, which gets filtered so as to only return values of type int. Lament takes the return value and dumps it to the new config file (currently implemented using JSON).

## The Lament Configuration

The name of this project comes from the puzzle box in the [Hellraiser movies](http://en.wikipedia.org/wiki/Lemarchand%27s_box).

## Licence

`lament` is released under the [Mozilla Public License Version 2.0](http://opensource.org/licenses/MPL-2.0).
