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
NEW Column
PUSH match
ATTR w
PUSH wrap
ATTR h
PUSH center
ATTR gravity
NEW Text
PUSH dp
PUSH 30
UNIT
ATTR w
PUSH dp
PUSH 20
UNIT
ATTR h
PUSH sp
PUSH 13
UNIT
ATTR textSize
PUSH user
PUSH name
PROP
CALL title
ATTR text
PUSH user
PUSH name
PROP
CALL len
DUP
STORE_TEMP
PUSH 0
PUSH_TEMP
CALL gt
ATTR visible
CALLBACK PUSH user>PUSH onClick>PROP
ATTR onClick
CALLBACK PUSH fview>PUSH fposition>PUSH user>PUSH onItemClick>PROP
ATTR onItemClick
ATTR child
NEW Image
PUSH default_portrait
PUSH drawable
RES
ATTR placeHolder
PUSH fitCenter
ATTR scaleType
PUSH user
PUSH portrait
PROP
DUP
STORE_TEMP
PUSH 40dp
PUSH 30dp
PUSH_TEMP
CALL scale
ATTR src
ATTR child
INCLUDE compile/resusable_layout.rvc
ATTR child
```