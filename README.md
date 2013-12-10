# Lament

An easy way to handle application configuration (and open a schism to a dimention of endless pain and suffering).

## Example

First you create a config parser by subclassing LamentConfig:

```
class Example(LamentConfig):
```

Then you can declare handlers for each config attribute. For example you could have 'attr' which takes a list of values:

```
    @config('attr', list)
    def update_a(self, config, obj):
        return obj
```

In the above example, the handler receives 'config' which is the current value of att and 'obj' which is the value found when you open a new config file. You're free to handle any changes to config that you see fit and the value you return will be set as the new value for that attribute. The above example is simply an override on the current value.

// TODO: Document exporting values

## The Lament Configuration

The name of this project comes from the puzzle box in the [Hellraiser movies](http://en.wikipedia.org/wiki/Lemarchand%27s_box).

## Licence

`lament` is released under the [Mozilla Public License Version 2.0](http://opensource.org/licenses/MPL-2.0).
