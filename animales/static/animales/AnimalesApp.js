(function(window, $) {
    window.AnimalesApp = function ($wrapper) {

        this.$wrapper = $wrapper;
        this.helper = new Helper(this.$wrapper);

        this.$wrapper.on(
            'click',
            'tbody tr',
            this.handleRowClick.bind(this)
        )

        this.$wrapper.on(
            'click',
            '.js-delete-row',
            this.handleComidaDelete.bind(this)
        )

        this.$wrapper.on(
            'submit',
            '.js-new-animales-form',
            this.handleNewFormSubmit.bind(this)
        )

        this.$wrapper.on(
            'click',
            '.js-update-row',
            this.handleUpdateFormSubmit.bind(this)
        )
    };

    $.extend(window.AnimalesApp.prototype, {
        handleRowClick: function () {
            console.log("Click en Fila");
        },

        handleComidaDelete: function (e) {
            e.preventDefault();

            let $link = $(e.currentTarget);

            $link.addClass('text-danger');
            $link.find('.fa')
                .removeClass('fa-trash')
                .addClass('fa-spinner')
                .addClass('fa-spin');

            let deleteUrl = $link.data('url');
            let $row = $link.closest('tr');
            let that = this;

            $.ajax({
                url: deleteUrl,
                method: 'POST',
                data: {csrfmiddlewaretoken: csrftoken}
            })
                .done(function (data) {
                    console.log(data);
                    $row.fadeOut('normal', function () {
                        $(this).remove();
                        that.updateTotalComida();
                    });
                })
                .fail(function () {
                    console.log("error");
                })
                .always(function () {
                    console.log("completado");
                });
        },

        updateTotalComida: function () {
            this.$wrapper.find('.js-total-comida').html(
                this.helper.calculateTotalComida()
            );
        },

        handleNewFormSubmit: function (e) {
            e.preventDefault();
            console.log("enviando");
            let $form = $(e.currentTarget);
            let $tbody = this.$wrapper.find('tbody');
            let that = this;
            $.ajax({
                url: $form.attr('action'),
                method: 'POST',
                data: $form.serialize()
            })
                .done(function(d) {
                    //$tbody.append(d);
                    that.updateTotalComida();
                })
                .fail(function() {
                    console.log("error");
                })
                .always(function() {
                    console.log("complete");
                });
        },

        handleUpdateFormSubmit: function (e) {
            e.preventDefault();

            let $link = $(e.currentTarget);
            
            if ($link.find('.fa-edit').length ===1){
                $link.addClass('text-blue');
                $link.find('.fa')
                    .removeClass('fa-edit')
                    .addClass('fa-save');
                
                let $row = $link.closest('tr');
                lista = $row.find('td')
                for (let index = 1; index < lista.length -1; index++) {
                    lista[index].setAttribute("contenteditable",true)
                }
            }else{
                $link.addClass('text-blue');
                $link.find('.fa')
                    .removeClass('fa-save')
                    .addClass('fa-edit');
                    let $row = $link.closest('tr');
                    lista = $row.find('td')
                    for (let index = 1; index < lista.length -1; index++) {
                        lista[index].setAttribute("contenteditable",false)
                        //console.log(lista[index].innerText)
                    }
                 datajson = {
                    'especie':lista[1].innerText,
                    'nombre':lista[2].innerText,
                    'numero':lista[3].innerText,
                    'comida':lista[4].innerText,
                    'id':lista[0].innerText,
                }
                
                that = this;
                json_data = JSON.stringify(datajson)
             
                 let updatedata = $link.data('url');
                 $.ajax({
                     url: updatedata,
                     method: 'POST',
                     data: json_data,
                     dataType: 'json',
                     contentType: 'application/json',
                 })
                     .done(function(d) {
                         //$tbody.append(d);
                         that.updateTotalComida();
                     })
                     .fail(function() {
                         console.log("error");
                     })
                     .always(function() {
                         console.log("complete");
                     });
                 
                     
                 //let that = this;
                
            }
        }
    });

    
    let Helper = function ($wrapper) {
        this.$wrapper = $wrapper
    };

    $.extend(Helper.prototype, {
        calculateTotalComida : function () {
            let total = 0;
            this.$wrapper.find('tbody tr').each(function () {
                if (undefined !== $(this).data('comida')) {
                     total += parseInt($(this).data('comida'));
                }
            });
            return total;
        }
    });

})(window, jQuery);
