gz = require './helpers'

class ListView extends gz.GView
    el : $ \body

    events :
        'click button.add' : ->
            @counter++
            $(\ul, @el).append "<li>Hola #{@counter}</li>"

    initialize : ->
        @counter = 0
        @render!

    render : ->
        $(@el).append "<button class='add'>Agregar</button>"
        $(@el).append '<ul></ul>'

listView = new ListView
