## ReactiveView for Mobile develop

### 语法
```
# this is comment

Column {
    w: match
    h: wrap
    gravity: center
    child: Text {
        w: 30dp
        # should use wrap
        h: 20dp
        textSize: 13sp
        text: {user.name |> title}
        visible: {user.name |> len |> gt $, 0}
        onClick: {-> user.onClick}
        onItemClick: {view, position -> user.onItemClick}
    },
    child: Image {
        placeHolder: @drawable/default_portrait
        scaleType: fitCenter
        src: {user.portrait |> scale $, 30dp, 40dp}
    }
    child: include(resusable_layout.rv)
}
```

### stack-base 虚拟机指令

```
PUSH Column
NEW
PUSH match
PUSH w
ATTR
PUSH wrap
PUSH h
ATTR
PUSH center
PUSH gravity
ATTR
PUSH Text
NEW
PUSH dp
PUSH 30
UNIT 30
PUSH w
ATTR
PUSH dp
PUSH 20
UNIT 20
PUSH h
ATTR
PUSH sp
PUSH 13
UNIT 13
PUSH textSize
ATTR
PUSH user
PUSH name
PROP
PUSH title
CALL
PUSH text
ATTR
PUSH user
PUSH name
PROP
PUSH len
CALL
DUP
STORE_TEMP
PUSH 0
PUSH_TEMP
PUSH gt
CALL
PUSH visible
ATTR
PUSH compile/dsl$1.rvc
CALLBACK
PUSH onClick
ATTR
PUSH compile/dsl$1.rvc
CALLBACK
PUSH onItemClick
ATTR
PUSH child
ATTR
PUSH Image
NEW
PUSH default_portrait
PUSH drawable
RES
PUSH placeHolder
ATTR
PUSH fitCenter
PUSH scaleType
ATTR
PUSH user
PUSH portrait
PROP
DUP
STORE_TEMP
PUSH 40dp
PUSH 30dp
PUSH_TEMP
PUSH scale
CALL
PUSH src
ATTR
PUSH child
ATTR
PUSH compile/resusable_layout.rvc
INCLUDE
PUSH child
ATTR
```