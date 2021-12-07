# Paint for Handwritten Dataset

## Requirements

* Image Magick >= 6.0
* poetry

You can build the environment using poetry below:

``` bash
poetry install
```

You have to change `etc/ImageMagick-6/policy.xml`.

before change

```
<policy domain="coder" rights="none" pattern="PS" />
<policy domain="coder" rights="none" pattern="PDF" />
```

after

```
<policy domain="coder" rights="read|write" pattern="PS" />
<policy domain="coder" rights="read|write" pattern="PDF" />
```



## To Do

* ImageMagickを使いたくない
