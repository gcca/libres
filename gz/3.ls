gz = require './helpers'

class Item extends gz.GModel
    defaults :
        nombre   : 'hola'
        apellido : 'mundo'


class List extends gz.GCollection
    model : Item


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
        $(\ul, @el).append "<li>#{item.get \nombre} #{item.get \apellido}</li>"

listView = new ListView
