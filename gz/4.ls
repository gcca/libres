gz = require './helpers'

class Item extends gz.GModel
    defaults :
        nombre   : 'hola'
        apellido : 'mundo'


class List extends gz.GCollection
    model : Item


class ItemView extends gz.GView
    tagName : \li  # nombre del tag en `@el`

    initialize : ->
        # Sin cuerpo

    render : ->
        $(@el).html "<span>#{@model.get \nombre} #{@model.get \apellido}</span>"
        @  # para invocaciones en cadena: *.render().el


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
        @collection.bind \add, @appendItem  # Asociar evento 'add'.
                                            # Cada vez que se agregue un elemento
                                            # a `@collection`, se invocará
                                            # a la función `@appendItem`
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
