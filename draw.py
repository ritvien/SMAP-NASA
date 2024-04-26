from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
import random
import matplotlib.pyplot as plt

def draw_plot(data,plot_title):
    plot(range(len(data)),data,alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

def draw_xvline(segments):
    for seg in segments:
        x0 = seg[0]
        plt.axvline(x=x0)
        
def draw_approximate_line(ax_set):
    fig, axs = plt.subplots(1,1, figsize=(25, 5))
    x0,y0,x1,y1 = ax_set[0]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for ax in ax_set:
        axs.plot((x1,ax[0]),(y1,ax[1]),ls='--',color='black',alpha=0.5)
        x0,y0,x1,y1 = ax
        axs.plot((x0,x1),(y0,y1),alpha=1,color=random.choice(colors))
    plt.show();

    
def count_lines(df):
    '''
    
    Return (int,array)
        int : number of anomaly line
        array : anomaly points, split by each line
    Parameters
        df : each batch
        
    '''
    anomaly_idx = df[df['label'] == 1].index
    anomaly_sequences = []
    anomaly_sequence = [anomaly_idx[0]]

    for i in range(1,len(anomaly_idx)):
        if anomaly_idx[i] == anomaly_idx[i-1]+1:
            anomaly_sequence.append(anomaly_idx[i])
        else:
            anomaly_sequences.append(anomaly_sequence)
            anomaly_sequence = [anomaly_idx[i]]
    return len(anomaly_sequences),anomaly_sequences    

def plot_anomalies(df,num_batch):
    num_line, points = count_lines(df)
    fig, axs = plt.subplots(1, 1, figsize=(20,5))
    axs.plot(df['value'],label='Normal')
    
    for i in range(num_line):
        start_anomaly = points[i][0] 
        end_anomaly = points[i][-1] 
        anomaly_df = df.iloc[start_anomaly:end_anomaly]
        axs.plot(anomaly_df['value'],
                 label='Anomaly',
                 c='tomato',
                 linewidth=5,
                 alpha=0.8)
    axs.set_xlabel('Time')
    axs.set_ylabel('Value')
    axs.set_title(f'Batch: {num_batch}')
    axs.legend(labels=['Normal', 'Anomaly'])
    plt.show();
    
def plot_anomaly(df,num_batch):
    
    """
    Plot the longest anomaly sequences
    """
    
    num_line, points = count_lines(df)
    longest_sequence = max(points, key=len)

    fig, axs = plt.subplots(1, 1, figsize=(20,5))
    axs.plot(df['value'],label='Normal')
    
    start_index = df.index[0]
    start_anomaly = longest_sequence[0] - start_index 
    end_anomaly = longest_sequence[-1] - start_index
    anomaly_df = df.iloc[start_anomaly:end_anomaly]
    axs.plot(anomaly_df['value'],
             label='Anomaly',
             c='tomato',
             linewidth=5,
             alpha=0.8)
    axs.set_xlabel('Time')
    axs.set_ylabel('Value')
    axs.set_title(f'Batch: {num_batch}')
    axs.legend(labels=['Normal', 'Anomaly'])
    plt.show();