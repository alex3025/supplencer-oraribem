class converter:
    def convert_days(mode, first):
        if mode == 1:
            if first == 'Monday':
                return '1'
            elif first == 'Tuesday':
                return '2'
            elif first == 'Wednesday':
                return '3'
            elif first == 'Thursday':
                return '4'
            elif first == 'Friday':
                return '5'
            elif first == 'Saturday':
                return '6'
            elif first == 'Sunday':
                return '7'
        elif mode == 2:
            if first == '1':
                return 'Monday'
            elif first == '2':
                return 'Tuesday'
            elif first == '3':
                return 'Wednesday'
            elif first == '4':
                return 'Thursday'
            elif first == '5':
                return 'Friday'
            elif first == '6':
                return 'Saturday'
            elif first == '7':
                return 'Sunday'
