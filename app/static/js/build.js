import Alpine from 'alpinejs'
import focus from '@alpinejs/focus'
import collapse from '@alpinejs/collapse'
import mask from '@alpinejs/mask'

window.Alpine = Alpine

Alpine.plugin(focus)
Alpine.plugin(collapse)
Alpine.plugin(mask)

Alpine.start()
