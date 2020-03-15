$(function() {
    $('ul.navbar-nav').prepend('<li class="nav-item"><a  id="form-open" class="nav-link" href="">追加 </a></li>');

    function adjustImage() {
        const imageWrapper = $('.image__wrapper');
        imageWrapper.css({
            height: `${imageWrapper.width()}px`
        });

        const image = $('img.user__icon');
        if (image.width() >= image.height()) {
            image.css({
                height: '100%',
                width: 'auto'
            });
        } else {
            image.css({
                height: 'auto',
                width: '100%'
            });
        }
    }

    adjustImage();

    $('label').hide();
    $('textarea').attr('placeholder', '質問を入力してください');
    for (let i = 0; i < 2; i++) {
        $(`input#id_choices-${i}-choice`).attr({
            'placeholder': `回答${i+1}`,
            'autocomplete': 'off'
        });
    }

    for (let i = 0; i < 4; i++) {
        $('select[name="minute"]').append($('<option>').val(`${15*i}`).text(`${15*i}`).attr('size', '5'))
    }
    for (let i = 0; i < 24; i++) {
        $('select[name="hour"]').append($('<option>').val(`${1*i}`).text(`${1*i}`))
    }
    for (let i = 0; i < 7; i++) {
        $('select[name="day"]').append($('<option>').val(`${1*i}`).text(`${1*i}`))
    }

    $(document).on('click','div.question-area div.detail span.status', function() {
        const questionPK = $(this).parents('div.question-area').attr('id');
        if ($(this).attr('class') === 'status') {
            $(`div#${questionPK}.choice-area`).hide();
            $(`div.question-area#${questionPK}`).css({
                height: '380px',
            });
            $(`div.question-area#${questionPK} p`).css({
                height: 'calc(100% - 2em)',
                overflow: 'scroll',
                overflowX: 'hidden'
            });
            $(this).addClass('off');
            $(this).html('隠す');
            $(this).parent().children('.dot').hide();
        } else {
            $(`div#${questionPK}.choice-area`).show();
            $(`div.question-area#${questionPK}`).css({
                height: '190px',
            });
            $(`div.question-area#${questionPK} p`).css({
                height: '100%',
                overflow: 'hidden'
            });
            $(this).removeClass('off');
            $(this).html('全て表示');
            $(this).parent().children('.dot').show();
        }
    });

    // {#$('a.choice').hover(#}
    // {#    function() {#}
    // {#        $(this).stop().animate({height: 'calc(0.5rem*2 + 1.5rem*2)'}, 100);#}
    // {#    },#}
    // {#    function() {#}
    // {#        $(this).stop().animate({height: 'calc(0.5rem*2 + 1.5rem)'}, 100);#}
    // {#    }#}
    // {#);#}

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $('form#create').submit(function(e) {
        e.preventDefault();
        // {#const choicesHtml = $('input[name^="choices"][type="text"]');#}
        // {#var choicesList = [];#}
        // {#choicesHtml.each(function() {#}
        // {#const val = $(this).val();#}
        // {#    choicesList.push(val);#}
        // {# });#}
        // {#const choices = choicesList.join('/');#}
        // {#console.log(choices);#}

        const setChoicesHtml = $('input[name^="choices"][type="text"]');
        let setChoices = [];
        setChoicesHtml.each(function() {
            setChoices.push($(this).val())
        });
        setChoices = setChoices.filter(Boolean);

        const deadlineChecker = Number($('select[name="day"]').val() + $('select[name="hour"]').val() + $('select[name="minute"]').val());
        console.log(deadlineChecker);

        if (setChoices.length >= 2 && deadlineChecker) {
            $.ajax({
                'url': '{% url 'cms:form' %}',
                'type': 'POST',
                'data': $(this).serialize(),
                'beforeSend': function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                 }}
            }).done(function(response) {
                $('.form__modal').fadeOut();
                $('.container-fluid').attr('style', '');
                $('html, body').prop({scrollTop: pos});
                $('textarea').val('');
                const choicesHtml = $('input[name^="choices"][type="text"]');
                choicesHtml.each(function() {
                   $(this).val('');
                });
                $('div#form-choice-area').popover('dispose');
                $('select[name="minute"]').popover('dispose');

                const created = response.created;
                const problem = response.problem;
                console.log(created);
                console.log(problem);
            })
        } else if (setChoices.length >= 2) {
            $('select[name="minute"]').popover({
                content: '期間を指定してください',
                placement: 'right',
            });
            $('select[name="minute"]').popover('show');
        } else {
            $('div#form-choice-area').popover({
                content: '質問は２つ以上必要です',
                placement: 'bottom',
            });
            $('div#form-choice-area').popover('show');
        }
    });

    var deadlineList = [];
    {% for deadline in deadlines %}
        var endTime = new Date('{{ deadline }}');
        deadlineList.push(endTime);
    {% endfor %}

    var localDeadlineList = [];
    {% for local in local_deadlines %}
        var localEndTime = new Date('{{ local }}');
        localDeadlineList.push(localEndTime);
    {% endfor %}

    var addZero = function(n) {
        return ('0' + n).slice(-2);
    };

    function countdownTimer(deadline, local, n) {
        var nowTime = new Date();
        if (nowTime > local) { //なぜかifではローカルタイムが考慮されない
            $('.timer').eq(n).text('expired');
        } else {
            var calc =  new Date(deadline - nowTime);//ここでは時間が合わせられる
            var date = calc.getDate() - 1 ? calc.getDate() - 1 + '日' : ''; //? = if
            var hours = calc.getHours() ? calc.getHours() + '時間' : '';
            var minutes = addZero(calc.getMinutes()) + '分';
            {#var seconds = addZero(calc.getSeconds()) + '秒';#}
            $('.timer').eq(n).text(`${date + hours + minutes}`);
        };
    }

    function repeater() {
        for (let i = 0; i < deadlineList.length; i++) {
            countdownTimer(deadlineList[i], localDeadlineList[i], i);
        }
    }
    repeater();
    setInterval(repeater, 60000);

    var loadedCount = 0;
    $('#plus button').click(function(e) {
        e.preventDefault();
        loadedCount += 1;

        let displayedQuestionsPk = [];
        $('div.choice-area').each(function() {
            const pk = $(this).attr('id');
            displayedQuestionsPk.push(pk);
        });
        const strDisplayedQuestionsPk = displayedQuestionsPk.join('/');

        $.ajax({
            'url': '{% url 'cms:add' %}',
            'type': 'GET',
            'data': {
                'loaded_count': loadedCount,
                'displayed': strDisplayedQuestionsPk,
            },
            'dataType': 'json'
        }).done(function(response) {
            const zeroCheck = response.not_zero;
            if (zeroCheck) {
                const questionPkList = response.question_pk_list;
                const textList = response.text_list;
                const userList = response.user_list;
                const imageList = response.image_list;
                const totalList = response.total_list;
                const choicesList = response.choices_list;
                const choicePksList = response.choice_pks_list;
                const ratesList = response.rates_list;
                const votedCheck = response.voted_check;
                const votedChoicePks = response.voted_choice_pks;

                for (let i = 0; i < questionPkList.length; i++) {
                    $('div.base').append(`
                        <div class="sheet col-xl-4 col-md-6">
                          <div class="sheet-content shadow-sm rounded-lg">
                            <div class="top-area">
                              <span class="image__wrapper image__mini">
                                <img class="user__icon" src="${imageList[i]}" />
                              </span>
                              <span class="username">${userList[i]}</span>
                                <span class="timer-wrapper mt-1">残り　<span class="timer"></span></span>
                            </div>
                            <div id="${questionPkList[i]}" class="question-area mt-2 mb-2">
                              <p class="question-text">${textList[i]}</p>
                                <div class="detail">
                                    <span class="dot">...</span>
                                    <span class="status">全て表示</span>
                                </div>
                            </div>
                            <hr class="hr1">
                            <div id="${questionPkList[i]}" class="choice-area">
                            </div>
                            <div id="${questionPkList[i]}" class="bottom__area">
                              <span class="total">投票数 ${totalList[i]}</span>
                            </div>
                          </div>
                        </div>
                    `);
                    if (votedCheck[i]) {
                        for (let j = 0; j < choicePksList[i].length; j++) {
                            $(`div#${questionPkList[i]}.choice-area`).append(`
                                <a href="#" id="${choicePksList[i][j]}" class="choice choice-${questionPkList[i]}">${choicesList[i][j]}</button>
                            `)
                        }
                    } else {
                        for (let j = 0; j < choicePksList[i].length; j++) {
                            $(`div#${questionPkList[i]}.choice-area`).append(`
                                <div class="result-area"  id="result__${choicePksList[i][j]}">
                                    <span class="choice__text">${choicesList[i][j]}</span>
                                    <span class="rate">${ratesList[i][j]}%</span>
                                </div>
                            `);
                            const eachResultArea = $(`#result__${choicePksList[i][j]}`);
                            if(votedChoicePks.indexOf(choicePksList[i][j]) !== -1 ) {
                                eachResultArea.css({
                                    'background': `linear-gradient(90deg,
                                    hsla(180,60%,50%,1) 0%,hsla(180,60%,50%,1) ${ratesList[i][j]}%,
                                    hsla(180,100%,98%,1) ${ratesList[i][j]}%,hsla(180,100%,98%,1) 100%)`
                                });
                            } else {
                                eachResultArea.css({
                                    'background': `linear-gradient(90deg,
                                    hsla(200,30%,80%,1) 0%,hsla(200,30%,80%,1) ${ratesList[i][j]}%,
                                    hsla(200,20%,98%,1) ${ratesList[i][j]}%,hsla(200,20%,98%,1) 100%)`
                                });
                            }
                        }
                    }
                }
                adjustImage();
                repeater();
            }else {
                $('#plus').empty();
            }
        })
    });

    // 後から追加した質問にも対応できる記述↓
    $(document).on('click', 'a.choice', function(e) {
        e.preventDefault();
        const selectedPk = $(this).attr('id');
        const questionPk = $(this).parents('div.choice-area').attr('id');
        const choiceArea = $(`div#${questionPk}.choice-area`);
        const choices = $(`a.choice-${questionPk}`);

        $.ajax({
            'url': '{% url 'cms:vote' %}',
            'type': 'GET',
            'data': {
                'choice_pk': selectedPk,
                'question_pk': questionPk,
            },
            'dataType': 'json'
        }).done(function(response) {
            choiceArea.empty();
            const votesRateList = response.rates_list;
            const total = response.total_num;
            console.log(total);

            $(`#${questionPk}.bottom__area`).children('.total').text(`投票数 ${total}`);

            for (let i = 0; i < votesRateList.length; i++) {
                const choiceText = choices.eq(i).text();
                const choiceId = choices.eq(i).attr('id');
                choiceArea.append(`
                      <div class="result-area"  id="result__${choiceId}">
                        <span class="choice__text">${choiceText}</span>
                        <span style="float: right">${votesRateList[i]}%</span>
                      </div>
                `);
                const eachResultArea = $(`#result__${choiceId}`);
                if (choiceId === selectedPk ){
                    eachResultArea.css({
                    'background': `linear-gradient(90deg,
                                    hsla(180,60%,50%,1) 0%,hsla(180,60%,50%,1) ${votesRateList[i]/2}%,
                                    hsla(180,100%,98%,1) ${votesRateList[i]/2}%,hsla(180,100%,98%,1) 100%)`,
                    'background-size': `200% 100%`,
                    'animation': 'graph 1s ease 1 forwards'
                    });
                } else {
                    eachResultArea.css({
                    'background': `linear-gradient(90deg,
                                    hsla(200,30%,80%,1) 0%,hsla(200,30%,80%,1) ${votesRateList[i]/2}%,
                                    hsla(200,20%,98%,1) ${votesRateList[i]/2}%,hsla(200,20%,98%,1) 100%)`,
                    'background-size': `200% 100%`,
                    'animation': 'graph 1s ease 1 forwards'
                    });
                }
            }
        })
    });

    var totalForms = $('input#id_choices-TOTAL_FORMS');
    var currentChoicesCount = parseInt(totalForms.val());
    $('a#add').click(function(e) {
        e.preventDefault();
        var setChoice = $('input.form-control');
        var name = setChoice.eq(1).attr('name').split('-');
        const partA = name[0];
        const partB = name[2];

        var extraChoice = $('<input>', {
            type: 'text',
            maxlength: setChoice.eq(1).attr('maxlength'),
            name: partA + '-' + currentChoicesCount + '-' + partB,
            id: 'id_' + partA + '-' + currentChoicesCount + '-' + partB,
            class: 'form-control',
            placeholder: `回答${currentChoicesCount+1}`,
            autocomplete: 'off'
        });
        extraChoice.css({
            'margin-bottom': '16px'
        });

        $('#form-choice-area').append(extraChoice);
        currentChoicesCount += 1;
        if (currentChoicesCount === 4) {
            $('div#add__area').remove();
        }
        totalForms.attr('value', currentChoicesCount);
    });

    function modalOpen(modal) {
        $(modal).fadeIn();
        pos = $(window).scrollTop();
        $('.container-fluid').css({
            'position': 'fixed',
            'top': -1 * pos
        })
    }

    function modalClose(modal) {
        $(modal).fadeOut();
        $('.container-fluid').attr('style', '');
        $('html, body').prop({scrollTop: pos});
    }

    $('#form-open').on('click',function(e){
        e.preventDefault();
        modalOpen('.form__modal');
    });

    $('.modal__bg').on('click',function(e){
        e.preventDefault();
        modalClose('.__modal');
        $('div#form-choice-area').popover('dispose');
        $('select[name="minute"]').popover('dispose');
    });

});