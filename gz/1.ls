gz = require './helpers'

class ListView extends gz.GView
    el : $ \body

    initialize: ->
        @render!      # this.render()

    render : ->
        # $(@el).append('...')
        ($ @el).append '<ul><li>Hola</li></ul>'

listView = new ListView
