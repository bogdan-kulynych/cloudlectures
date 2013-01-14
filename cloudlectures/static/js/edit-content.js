(function($) {
    $(document).ready(function() {
        $unit_template    = $('#template li.unit');
        $lecture_template = $('#template li.lecture');
        $content_tree     = $('#content-tree');


        // Builds a tree from valid JSON representation
        function build_tree(json) {
            if (!json) {
                return;
            }

            var units = json["units"];

            for (var i = 0; i < units.length; ++i) {
                var unit     = units[i],
                   $unit     = add_unit(unit["title"], unit["description"]);

                var lectures = unit["lectures"];
                
                if (lectures) {
                    for (var j = 0; j < lectures.length; ++j) {
                        var lecture = lectures[j];
                        $lecture = add_lecture($unit, lecture.link, lecture.title,
                                    lecture.description);
                    }
                }
            }
        }


        // Returns JSON object corresonding to the tree
        function jsonify_tree() {
            var json = {
                units: []
            };

            $content_tree.find('.unit:not(.removed)').each(function() {
                var $this       = $(this);
                var title       = $this.find('> .fields > .title .value')
                                       .text(),
                    description = $this.find('> .fields > .description .value')
                                       .text(),
                   $lectures    = $this
                                  .find('> .fields > .lectures .lecture:not(.removed)');

                var lectures    = [];

                $lectures.each(function() {
                    var $this = $(this);
                    var link  = $this
                        .find('> .fields > .media-body .link .value').text(),
                        title = $this
                        .find('> .fields > .media-body .title .value').text(),
                        description = $this
                        .find('> .fields > .media-body .description .value')
                                 .text();

                    lectures.push({
                        "link": link,
                        "title": title,
                        "description": description
                    });
                });

                json.units.push({
                    "title": title,
                    "description": description,
                    "lectures": lectures
                });
            });

            return json;
        }


        // New unit
        function add_unit(title, description) {
            // Adding unit to DOM
            $content_tree.append($unit_template.clone());
            $unit = $content_tree.find('.unit:last-child');

            // Setting values
            if (title) {
                $unit.find('.title .value').text(title);
            }
            if (description) {
                $unit.find('.description .value').text(description || '');
            }

            // Sortable
            $content_tree.sortable({
                placeholder: 'well drop-placeholder',
                cursor: 'move',
                cancel: '.removed',
                delay: 200,
                axis: "y"
            });

            // Enable text selection on inputs
            $content_tree.on('mousedown.ui-disableSelection selectstart.ui-disableSelection',
                             'input', function(e) {
                e.stopImmediatePropagation();
            });

            // New lecture
            $unit.find('.lecture-add').click(function(e) {
                e.preventDefault();

                var $unit = $(this).closest('.unit');
                add_lecture($unit);
            });

            return $unit;
        }


        // New lecture
        function add_lecture($unit, link, title, description) {
            $lectures = $unit.find('.lectures');

            // Adding lecture to DOM
            $lectures.append($lecture_template.clone());
            $lecture = $lectures.find('.lecture:last-child');

            // Setting values
            if (link) {
                $lecture.find('.link .value').text(link);
            }
            if (title) {
                $lecture.find('.title .value').text(title);
            }
            if (description) {
                $lecture.find('.description .value').text(description);
            }

            // Sortable
            $lectures.sortable({
                placeholder: 'well-small drop-placeholder',
                cursor: 'move',
                cancel: '.removed',
                delay: 200,
                axis: "y"
            });

            // Enable text selection on inputs
            $lectures.on('mousedown.ui-disableSelection selectstart.ui-disableSelection',
                             'input', function(e) {
                e.stopImmediatePropagation();
            });

            // Updating ajax
            if (link) {
                update_preview($lecture,
                               $lecture.find('.link'),
                               link,
                               false);
            }

            return $lecture;
        }

        // Update lecture thumbnail
        function update_preview($lecture, $field, newValue, force) {
            var vid = youtube_parser(newValue);
            var url = 'http://gdata.youtube.com/feeds/api/videos/' +
                       vid + '?v=2&alt=jsonc&format=5';
            $.ajax({
                type: 'GET',
                dataType: 'json',
                url: url,
                timeout: 5000,
                success: function(response){
                    var data = response.data;

                    var canonical = 'www.youtube.com/watch?v=' +
                                     data.id,
                        title = data.title,
                        description = data.description;

                    var $preview = $('<img class="media-object"/>')
                            .attr('src', data.thumbnail.sqDefault);

                    $lecture.find('.preview').html($preview);
                    $lecture.find('.link .value').text(canonical);
                    if (force === true || force === null) {
                        $lecture.find('.title .value').text(title);
                        $lecture.find('.description .value')
                                .text(description);
                    }

                    $field.removeClass('ajax-error');
                    $field.addClass('ajax-success');
                },
                error: function(xhr, textStatus, errorThrown) {
                    $field.removeClass('ajax-success');
                    $field.addClass('ajax-error');
                }
            });
        }

        // ============================================================================

        // Build initial tree

        var data = $('input#json-data').val();
        build_tree($.parseJSON(data));


        // 'Add unit' button
        $('.unit-add').click(function(e) {
            e.preventDefault();
            add_unit();
        });


        // 'Remove' button
        $content_tree.on('click', '.unit .remove', function(e) {
            e.preventDefault();

            $container = $(this).closest('.lecture, .unit');
            $container.addClass('removed');
            $container.find('> .fields').hide();

            var $rcontainer = $container.find('> .remove-container');
            $rcontainer.find('.normal').addClass('hidden');
            $rcontainer.find('.undo').removeClass('hidden');

            var $mcontainer = $container.find('> .resize-container');
            $mcontainer.addClass('hidden');

            // 'Undo' button
            $rcontainer.find('.remove-undo').click(function(e) {
                e.preventDefault();

                var $container = $(this).closest('.lecture, .unit');
                $container.removeClass('removed');
                $container.find('> .fields').show();

                var $rcontainer = $container.find('> .remove-container');
                $rcontainer.find('.normal').removeClass('hidden');
                $rcontainer.find('.undo').addClass('hidden');

                var $mcontainer = $container.find('> .resize-container');
                $mcontainer.removeClass('hidden');
            });

            // 'Remove for sure' button
            $rcontainer.find('.remove-sure').click(function(e) {
                e.preventDefault();

                var $container = $(this).closest('.lecture, .unit');
                $container.remove();
            });
        });
        

        // 'Resize' button
        $content_tree.on('click', '.unit .minimize', function(e) {
            e.preventDefault();

            var $unit = $(this).closest('.unit');
            $unit.find('> .fields > *:not(.title)').hide();

            var $mcontainer = $unit.find('.resize-container');
            $mcontainer.find('.normal').addClass('hidden');
            $mcontainer.find('.fullsize').removeClass('hidden')
                      .find('.maximize').click(function(e) {
                e.preventDefault();

                var $unit = $(this).closest('.unit');
                $unit.find('> .fields > *').show();

                var $mcontainer = $unit.find('.resize-container');
                $mcontainer.find('.normal').removeClass('hidden');
                $mcontainer.find('.fullsize').addClass('hidden');
            });

        });


        // 'Edit field' button
        $content_tree.on('click', '.text-field .normal .value, .text-field .field-edit',
        function(e) {
            e.preventDefault();

            var $field  = $(this).closest('.text-field');
            var $normal = $field.find('.normal'),
                $edit   = $field.find('.edit');
            var $input  = $edit.find('input');

            $normal.addClass('hidden');

            $input.val($normal.find('.value').text());
            $edit.removeClass('hidden');

            // Trigger event on enter hits
            $('body').keypress(function(e) {
                if (e.which === 13 && $input.is(':focus')) {
                    $edit.find('.field-save').trigger('enterpress');
                }
            });

            // 'Save edits' button
            if ($field.hasClass('link')) {
                $edit.find('.field-save').bind('click enterpress', function(e) {
                    e.preventDefault();

                    var $lecture = $(this).closest('.lecture');
                    var $field   = $(this).closest('.text-field');

                    var $normal  = $field.find('.normal'),
                        $edit    = $field.find('.edit');

                    var newValue = $edit.find('input').val();
                    $normal.find('.value').text(newValue);

                    update_preview($lecture, $field, newValue, true);

                    $edit.addClass('hidden');
                    $normal.removeClass('hidden');
                });
            } else {
                $edit.find('.field-save').on('click enterpress', function(e) {
                    e.preventDefault();

                    var $field  = $(this).closest('.text-field'),
                        $normal = $field.find('.normal'),
                        $edit   = $field.find('.edit');

                    var newValue = $edit.find('input').val();
                    $normal.find('.value').text(newValue);

                    $edit.addClass('hidden');
                    $normal.removeClass('hidden');
                });
            }

            // 'Abort edits' button
            $edit.find('.field-edit-cancel').click(function(e) {
                e.preventDefault();

                var $field  = $(this).closest('.text-field'),
                    $normal = $field.find('.normal'),
                    $edit   = $field.find('.edit');

                $edit.addClass('hidden');
                $normal.removeClass('hidden');
            });
        });
        

        // 'Save' button
        $('#json-container input[type=submit]').click(function(e) {
            e.preventDefault();

            var data = JSON.stringify(jsonify_tree());
            $form = $('#json-container');
            $form.find('input#json-data').attr('value', data);
            $form.submit();
        });
    });
})(jQuery);