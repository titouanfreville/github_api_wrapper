from yaspin import kbi_safe_yaspin
from yaspin.spinners import Spinners


class Spinner():
    """
    MAke it spin
    """
    __allowed_spinners = {
        'earth': Spinners.earth,
        'arc': Spinners.arc,
        }

    def __init__(self, text="spin", color="red"):
        self.sp = kbi_safe_yaspin(text=text, color=color)

    def spin_except(self, action, description='', spinner='earth', color='red'):
        """
        Spin expecting action to not return. Match exceptions and set spinner to fail

        :param action:
        :type action:
        :param description:
        :type description:
        :param spinner:
        :type spinner:
        :param color:
        :type color:
        :return:
        :rtype:
        """
        self.sp.color = color
        self.sp.text = description
        self.sp.spinner = spinner
        try:
            with self.sp:
                action()
                self.sp.ok("✔️ ")
        except Exception as e:
            print(e)
            self.sp.fail("💥 ")

    def spin_val(self, action, description='', spinner='earth', color='red'):
        """
        Spin expecting action to return objects. Manage exception (print message and set spinner to fail

        :param action:
        :type action:
        :param description:
        :type description:
        :param spinner:
        :type spinner:
        :param color:
        :type color:
        :return:
        :rtype:
        """
        self.sp.color = color
        self.sp.text = description
        self.sp.spinner = self.__allowed_spinners[spinner]
        try:
            with self.sp:
                res = action()
                if res:
                    self.sp.ok("✔️ ")
                    return res

                self.sp.fail("💥 ")
                return None
        except Exception as e:
            print(e)
            self.sp.fail("💥 ")
            return None

    def spin_bool(self, action, description = '', spinner = 'earth', color = 'red'):
        """
        Spin expecting action to return a boolean value and NEVER FAIL (exception are not matched)

        :param action:
        :type action:
        :param description:
        :type description:
        :param spinner:
        :type spinner:
        :param color:
        :type color:
        :return:
        :rtype:
        """
        self.sp.color = color
        self.sp.text = description
        self.sp.spinner = spinner
        with self.sp:
            res = action()
            if res:
                self.sp.ok("✔️ ")
                return res

            self.sp.fail("💥 ")
            return None
