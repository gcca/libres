gz = require './helpers'

class Item extends gz.GModel
    defaults :
        nombre   : 'hola'
        apellido : 'mundo'


class List extends gz.GCollection
    model : Item


class ItemView extends gz.GView
    tagName : \li  # nombre del tag en `@el`

    events :
        'click span.swap' : ->
            swapped =
                nombre   : @model.get \apellido
                apellido : @model.get \nombre
            @model.set swapped

        'click span.delete' : ->
            @model.destroy!

    initialize : ->
        @model.bind \change, @render, @
        @model.bind \remove, @unrender, @

    render : ->
        $(@el).html "
            <span style='color:black;'>
              #{@model.get \nombre} #{@model.get \apellido}
            </span>
            &nbsp; &nbsp;
            <span class='swap' style='font-family:sans-serif;
                                      color:blue;
                                      cursor:pointer;'>
              [swap]
            </span>
            <span class='delete' style='cursor:pointer;
                                        color:red;
                                        font-family:sans-serif;'>
              [delete]
            </span>"
        @  # para invocaciones en cadena: *.render().el

    unrender : ->
        $(@el).remove!


class ListView extends gz.GView
    el : $ \body

    events :
        'click button.add' : ->
            @counter++
            item = new Item
            item.set do
                apellido : (item.get \apellido) + ' ' + @counter
            @collection.add item

    initialize : ->
        @collection = new List
        @collection.bind \add, @appendItem

        @counter = 0
        @render!

    render : ->
        self = @  # self = this
        $(@el).append "<button class='add'>Add item</button>"
        $(@el).append '<ul></ul>'

        for item in @collection.models
            self.appendItem item

    appendItem : (item) ->
        itemView = new ItemView do  # `do` porque le estoy pasando un JSON
            model : item
        $(\ul, @el).append itemView.render!.el
        # recuerda que `func!` es lo mismo que `func()`

listView = new ListView
