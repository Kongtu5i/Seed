# Seed
> Get world seed without op permission.

## Preview

![image](https://user-images.githubusercontent.com/106148777/226171691-12bcd497-35a6-4680-a113-b5754f0d435b.png)

## Configure

`config/seed/config.json`
- `command`: Command to get seed in console
- `parser`: Parser for the command result

Default config file:
```
{
    'command': 'seed',
    'parser': 'Seed: [{}]'
}
```

The default configuration already supports most server software (without plugin/mods).

Both the legacy `Seed: [123]` output and Minecraft 26.3's
`System chat: Seed: [123]` output are supported. Existing configuration files
do not need to be changed. Custom parsers are tried against the original
output first, then against the output without the `System chat: ` prefix.

## Install / upgrade

Replace the existing Seed plugin in MCDR's `plugins` directory with
`seed-v1.2.1.mcdr`, then run `!!MCDR plugin reload seed`.
Use `!!seed` in game to check the result.

## Tests

With MCDReforged installed, run:

```sh
python -m unittest discover -s tests -v
```

## Thanks to

This plugin was inspired by [`MCDReforged/Seed`](https://github.com/MCDReforged/Seed)

Thanks to @[alex3236](https://github.com/alex3236) for refactoring the code（（
