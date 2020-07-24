from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from .forms import PredictionForm
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from plotly.offline import plot
from plotly.graph_objs import Figure,Scatter,Line,Data,Layout
def index(request):
    if request.method == "POST":
        prediction=PredictionForm(request.POST)
        if prediction.is_valid():
            speed=prediction.cleaned_data['speed']
            therotic=prediction.cleaned_data['therotic']
            direction=prediction.cleaned_data['direction']
            dataset = pd.read_csv('T1.csv')
            features_intake = ['LV ActivePower (kW)', 'Wind Speed (m/s)', 'Theoretical_Power_Curve (KWh)',
                               'Wind Direction (°)']
            features = dataset[features_intake]
            features.index = dataset['Date/Time']
            dataset = features.values
            data_in = dataset[:, 1:4]
            data_out = dataset[:, 0]
            try:
                speed = float(speed)
                therotic = float(therotic)
                direction = float(direction)
            except:
                return render(request, 'weather/index.html', {'form':prediction,'msg1':'Enter Numeric Values'})
            user = np.array([speed, therotic, direction])
            user = np.reshape(user, (1, -1))
            data_total = np.concatenate((data_in, user))
            scale = MinMaxScaler(feature_range=(0, 1))
            data_out = np.reshape(data_out, (-1, 1))
            data_in = scale.fit_transform(data_total)
            data_out = scale.fit_transform(data_out)
            lis = []
            for i in range(1, 121):
                lis.append(data_in[-i, :])
            data = np.array(lis)
            model = load_model('saved_model_result/final_model.h5')
            x_train = np.reshape(data, (1, 120, 3))
            x = model.predict(x_train)
            pred = scale.inverse_transform(x)[0][:]
            hour = np.argmax(pred)
            max_power = pred[hour]
            trace = Scatter(x=np.arange(1, 200), y=pred, fill='tonexty', fillcolor='orange', marker={'color': 'green'})
            data = Data([trace])
            layout = Layout(title='The  Predicted Wind Power in 72 Hours Future is', xaxis={'title': 'Hours'},
                            yaxis={'title': 'Power'})
            fig = Figure(data=data, layout=layout)
            fig.update_layout(legend_title=dict(text='Hours', font=dict(color='blue')))
            div = plot(fig, auto_open=False, output_type='div')
            return render(request, 'weather/index.html',
                          {'speed': div, 'form': prediction, 'hour': hour + 1, 'max_power': max_power,
                           'msgg1': 'The Maximum Predicted Power is At ', 'msgg2': 'hours in future with power :'})

    else:
        prediction=PredictionForm()
        return render(request,'weather/index.html',{'form':prediction})


