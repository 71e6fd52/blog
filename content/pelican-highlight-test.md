Title: pelican highlight test
Date: 2018-02-10 10:25:40
Author: yahvk
Category: Pelican
Tags: Pelican
Summary: Test pelican highlight

Outside a list:

::: version:

    :::python
    print("foo")

\`\`\` version:

```python
print("foo")
```

\#\! version:

    #!python
    print("foo")


Inside a list:

1. ::: version:

    Only four spaces to indent:

    :::python
    print("foo")

    Using eight spaces to indent:

        :::python
        print("foo")

2. \`\`\` version:

    Only four spaces to indent:

    ```python
    print("foo")
    ```

    Using eight spaces to indent:

        ```python
        print("foo")
        ```

3. #! version:

    Only four spaces to indent:

    #!python
    print("foo")

    Using eight spaces to indent:

        #!python
        print("foo")
