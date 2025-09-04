import pytest
from model import Question


# Fixtures para reutilização em testes
@pytest.fixture
def simple_question():
    """Fixture que cria uma questão simples"""
    return Question(title='Test Question')

@pytest.fixture
def question_with_multiple_choices():
    """Fixture que cria uma questão com várias choices"""
    question = Question(title='Multiple Choice Test', max_selections=2)
    question.add_choice("Option A", False)
    question.add_choice("Option B", True)
    question.add_choice("Option C", True)
    question.add_choice("Option D", False)
    return question

@pytest.fixture
def high_value_question():
    """Fixture que cria uma questão de alto valor"""
    return Question(title='Important Question', points=75, max_selections=3)


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
# Commit 2: Creating 10 unit tests
    
def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a'*120)
         
def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=-10)
    with pytest.raises(Exception):
        Question(title='q1', points=110)
        
def test_remove_specified_choice():
    question = Question(title='q1')
    
    question.add_choice("a", True)
    question.add_choice("b", False)
    
    choiceId = question.choices[0].id
    question.remove_choice_by_id(choiceId)
    
    assert len(question.choices) == 1
    assert question.choices[0].id != choiceId
    
def test_remove_all_choices():
    question = Question(title='q1')
    
    question.add_choice("a", True)
    question.add_choice("b", False)
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0
    
def test_remove_choice_by_invalid_id():
    question = Question(title='q1')
    
    question.add_choice("a", True)
    question.add_choice("b", False)
    
    choiceId = question.choices[0].id
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(choiceId + 10)
    

def test_set_single_correct_choice():
    question = Question(title='q1')
    
    correctChoice = question.add_choice("a", False)
    question.add_choice("b", False)
    
    assert not question.choices[0].is_correct
    assert not question.choices[1].is_correct
    
    question.set_correct_choices([correctChoice.id])
    
    assert question.choices[0].is_correct
        
def test_set_multiple_correct_choices():
    question = Question(title='q1')
    
    correctChoice1 = question.add_choice("a", False)
    question.add_choice("b", False)
    correctChoice2 = question.add_choice("c", False)
    correctChoiceIds = [correctChoice1.id, correctChoice2.id]
    
    question.set_correct_choices(correctChoiceIds)
    
    assert question.choices[0].is_correct 
    assert not question.choices[1].is_correct
    assert question.choices[2].is_correct
    
def test_set_invalid_correct_choice_id():
    question = Question(title='q1')
    
    question.add_choice("a", False)
    invalidChoice = question.add_choice("b", False)
    invalidChoiceId = invalidChoice.id
    
    question.remove_choice_by_id(invalidChoiceId)
    
    with pytest.raises(Exception):
        question.set_correct_choices([invalidChoiceId])
    
    
def test_correct_selection_with_no_correct_choices():
    question = Question(title='q1')
    
    question.add_choice("a", True)
    wrongChoice = question.add_choice("b", False)
    
    correctSelectedChoices = question.correct_selected_choices([wrongChoice.id])
    
    assert len(correctSelectedChoices) == 0
    
def test_correct_selection_with_all_correct_choices():
    question = Question(title='q1')
    
    correctChoice = question.add_choice("a", True)
    question.add_choice("b", False)
    
    correctSelectedChoices = question.correct_selected_choices([correctChoice.id])
    
    assert len(correctSelectedChoices) == 1
    assert correctSelectedChoices[0] == correctChoice.id

# Commit 3: Testing with fixtures

def test_question_can_receive_first_choice(simple_question):
    simple_question.add_choice("First option", True)
    
    assert len(simple_question.choices) == 1
    assert simple_question.choices[0].text == "First option"

def test_student_gets_score_when_selecting_all_correct_answers(question_with_multiple_choices):
    all_correct_ids = [choice.id for choice in question_with_multiple_choices.choices if choice.is_correct]
    
    score = question_with_multiple_choices.correct_selected_choices(all_correct_ids)
    
    assert len(score) == 2

def test_question_rejects_excessive_answer_selections(high_value_question):
    high_value_question.add_choice("Option 1", False)
    high_value_question.add_choice("Option 2", False) 
    high_value_question.add_choice("Option 3", False)
    high_value_question.add_choice("Option 4", False)
    
    too_many_selections = [choice.id for choice in high_value_question.choices]
    
    with pytest.raises(Exception) as exc_info:
        high_value_question.correct_selected_choices(too_many_selections)
    assert "Cannot select more than 3 choices" in str(exc_info.value)

