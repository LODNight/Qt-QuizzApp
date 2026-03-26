from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi
import sys
import json


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/tracNghiem.ui", self)

        # ===== STATE =====
        self.current_index = 0
        self.questions = []
        self.answered = False
        self.score = 0

        # ===== INIT =====
        self.loadData()
        self.setupButtons()
        self.showQuestion()
        self.widget_choice.hide()

        # ===== TIMER =====
        self.time_elapsed = 0  # tính bằng giây
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 1 giây chạy 1 lần

    # =========================
    # DATA
    # =========================
    def loadData(self):
        with open("data/tieuhoc.json", "r", encoding="utf-8") as file:
            self.questions = json.load(file)

    # =========================
    # TIMER
    # =========================
    def updateTime(self):
        self.time_elapsed += 1

        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60

        self.label_time.setText(f"Thời gian: {minutes:02}:{seconds:02}")

    # =========================
    # UI SETUP
    # =========================
    def setupButtons(self):
        self.buttons = {
            "A": self.btn_A,
            "B": self.btn_B,
            "C": self.btn_C,
            "D": self.btn_D
        }

        for key, btn in self.buttons.items():
            btn.clicked.connect(lambda _, k=key, b=btn: self.checkAnswer(k, b))

    # =========================
    # QUESTION FLOW
    # =========================
    def showQuestion(self):
        self.resetUI()
        self.answered = False

        question = self.questions[self.current_index]

        self.label_questionNumber.setText(f"Câu hỏi: {self.current_index + 1}")
        self.label_question.setText(question["question"])

        self.label_A.setText(question["a_answer"])
        self.label_B.setText(question["b_answer"])
        self.label_C.setText(question["c_answer"])
        self.label_D.setText(question["d_answer"])

    def nextQuestion(self):
        self.current_index += 1

        if self.current_index < len(self.questions):
            self.showQuestion()
        else:
            self.showResult()

    def showResult(self):
        self.timer.stop()
        
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60

        self.label_question.setText(
            f"🎉 Hoàn thành! \n" 
            f"Điểm: {self.score}/{len(self.questions)}\n"
            f"Thời gian: {minutes:02}:{seconds:02}"
        )
        self.label_questionNumber.setText("Kết thúc")

        self.widget_answer.hide()
        self.widget_choice.show()

        self.clearAnswers()

    # =========================
    # ANSWER LOGIC
    # =========================
    def checkAnswer(self, answer, button):
        if self.answered:
            return

        self.answered = True
        question = self.questions[self.current_index]

        correct = question["correct_answer"]

        if answer == correct:
            self.setButtonState(button, "correct")
            self.score += 1
        else:
            self.setButtonState(button, "wrong")
            self.setButtonState(self.buttons[correct], "correct")

        self.disableButtons()

        QTimer.singleShot(1000, self.nextQuestion)

    # =========================
    # UI STATE CONTROL
    # =========================
    def setButtonState(self, button, state):
        """
        state: correct | wrong | default
        """
        button.setProperty("state", state)
        button.style().unpolish(button)
        button.style().polish(button)

    def resetUI(self):
        for btn in self.buttons.values():
            self.setButtonState(btn, "default")
            btn.setEnabled(True)

    def disableButtons(self):
        for btn in self.buttons.values():
            btn.setEnabled(False)

    def clearAnswers(self):
        self.label_A.setText("")
        self.label_B.setText("")
        self.label_C.setText("")
        self.label_D.setText("")


# =========================
# RUN APP
# =========================
app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())